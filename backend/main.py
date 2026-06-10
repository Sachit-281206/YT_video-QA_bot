from fastapi import FastAPI
from models.request_models import (
    VideoRequest,
    QuestionRequest,
    SummaryRequest
)
from services.transcript_service import TranscriptService
from services.chunk_metadata_service import ChunkMetadataService
from services.embedding_service import EmbeddingService
from services.vector_store_service import VectorStoreService

# from services.qa_service_gemini import QAService
from services.qa_service_ollama import QAService
from utils.time_utils import seconds_to_mmss

from utils.youtube_utils import (
    extract_video_id
)
from services.summary_service import SummaryService

app = FastAPI(
    title="YouTube QA Bot API",
    description="Ask questions about YouTube videos using RAG",
    version="1.0.0"
)

embedding_service = EmbeddingService()
vector_store = VectorStoreService()
qa_service = QAService()
summary_service = SummaryService()

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.get("/")
def root():
    return {
        "message": "YouTube QA Bot API Running"
    }
    
@app.post("/process-video")
def process_video(
    request: VideoRequest
):

    video_id = extract_video_id(
        request.youtube_url
    )

    transcript = (
        TranscriptService.get_transcript(
            request.youtube_url
        )
    )

    chunks = (
        ChunkMetadataService
        .create_chunks_with_metadata(
            transcript,
            video_id
        )
    )

    embeddings = [
        embedding_service
        .generate_embedding(
            chunk["text"]
        )
        .tolist()
        for chunk in chunks
    ]

    vector_store.add_documents(
        chunks,
        embeddings
    )

    return {
        "message":
            "Video processed successfully",

        "video_id":
            video_id,

        "chunks_stored":
            len(chunks)
    }
    
@app.post("/ask")
def ask_question(
    request: QuestionRequest
):

    query_embedding = (
        embedding_service
        .generate_embedding(
            request.question
        )
        .tolist()
    )

    results = vector_store.search(
        query_embedding=query_embedding,
        video_id=request.video_id,
        n_results=5
    )

    documents = (
        results["documents"][0]
    )

    metadatas = (
        results["metadatas"][0]
    )

    answer = (
        qa_service.generate_answer(
            request.question,
            documents
        )
    )

    sources = []

    for metadata in metadatas:

        sources.append(
            {
                "start_seconds":
                    int(
                        metadata["start_time"]
                    ),

                "start_time":
                    seconds_to_mmss(
                        metadata["start_time"]
                    ),

                "end_time":
                    seconds_to_mmss(
                        metadata["end_time"]
                    )
            }
        )

    return {
        "answer": answer,
        "sources": sources
    }
    
@app.post("/summary")
def generate_summary(
    request: SummaryRequest
):

    results = (
        vector_store
        .get_video_chunks(
            request.video_id
        )
    )

    chunks = (
        results["documents"]
    )

    summary = (
        summary_service
        .summarize_video(
            chunks
        )
    )

    return {
        "summary": summary
    }