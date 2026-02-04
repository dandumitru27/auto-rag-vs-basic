import asyncio
import os

from lightrag.llm.gemini import gemini_complete_if_cache, gemini_embed
from lightrag.llm.openai import openai_complete_if_cache, openai_embed
from lightrag.utils import EmbeddingFunc
from raganything import RAGAnything, RAGAnythingConfig


async def main():
    # 1️⃣ Your API key & base URL
    provider = "openai"  # "google_genai" / "openai"

    if provider == "google_genai":
        api_key = os.getenv("GOOGLE_API_KEY")
    elif provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")

    # 2️⃣ Configure RAG-Anything
    config = RAGAnythingConfig(
        working_dir="./rag_storage",
        parser="docling",  # document parser (mineru or docling)
        parse_method="txt",  # auto/ocr/txt
        enable_image_processing=False,
        enable_table_processing=False,
        enable_equation_processing=False,
    )

    # 3️⃣ Define an LLM “model function”
    def llm_model_func(prompt, system_prompt=None, history_messages=[], **kwargs):
        if provider == "google_genai":
            return gemini_complete_if_cache(
                "gemini-2.5-flash",
                prompt,
                system_prompt=system_prompt,
                history_messages=history_messages,
                api_key=api_key,
                **kwargs,
            )
        elif provider == "openai":
            return openai_complete_if_cache(
                "gpt-5-mini",  # model name
                prompt,
                system_prompt=system_prompt,
                history_messages=history_messages,
                api_key=api_key,
                **kwargs,
            )

    # 4️⃣ Define an embedding function wrapper
    if provider == "google_genai":
        embedding_func = EmbeddingFunc(
            embedding_dim=768,  # dimension for gemini-embedding-001
            max_token_size=8192,
            func=lambda texts: gemini_embed(
                texts,
                model="models/gemini-embedding-001",
                api_key=api_key,
            ),
        )
    elif provider == "openai":
        embedding_func = EmbeddingFunc(
            embedding_dim=3072,  # dimension for text-embedding-3-large
            max_token_size=8192,
            func=lambda texts: openai_embed(
                texts,
                model="text-embedding-3-large",
                api_key=api_key,
            ),
        )

    # 5️⃣ Create RAG engine instance
    rag = RAGAnything(
        config=config,
        llm_model_func=llm_model_func,
        embedding_func=embedding_func,
    )

    # 6️⃣ Ingest documents
    # await rag.process_folder_complete(
    #     folder_path="C:\\Dev\\EPO_Patent_PDFs",
    #     output_dir="./output",
    #     file_extensions=[".pdf"],
    #     recursive=True,
    # )

    await rag.process_document_complete(
        file_path="C:\\Dev\\EPO_Patent_PDFs\\EP11869524NWA1.pdf", output_dir="./output"
    )

    # 7️⃣ Query
    # answer = await rag.query("What does section 3 of the document discuss?")
    # print(answer)

    print("Done.")


# Run
asyncio.run(main())
