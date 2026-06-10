class ChunkMetadataService:

    @staticmethod
    def create_chunks_with_metadata(
        transcript,
        video_id,
        snippets_per_chunk=20
    ):
        chunks = []

        for i in range(
            0,
            len(transcript),
            snippets_per_chunk
        ):

            batch = transcript[
                i:i + snippets_per_chunk
            ]

            text = " ".join(
                item.text
                for item in batch
            )

            start_time = batch[0].start

            end_time = (
                batch[-1].start +
                batch[-1].duration
            )

            chunks.append(
                {
                    "text": text,
                    "video_id": video_id,
                    "start_time": start_time,
                    "end_time": end_time
                }
            )

        return chunks