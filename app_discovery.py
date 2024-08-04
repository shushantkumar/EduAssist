import streamlit as st
from llama_parse import LlamaParse
import os
import pickle
import json
from pydantic import Field
from enum import Enum
import os
import openai

AI71_BASE_URL = "https://api.ai71.ai/v1/"
AI71_API_KEY = os.env.get("AI71_API_KEY")

client = openai.OpenAI(
    api_key=AI71_API_KEY,
    base_url=AI71_BASE_URL,
)


prompt_for_chapter = """Given a text chunk, analyze and identify all the chapters that can be made from it. For each chapter analyze it to identify whether it is complete or not. Determine a title for the chapter based on your understanding of the chunk. Identify the key concepts presented in the chapter that are essential for understanding the subject matter. Lastly, evaluate how well the chapter contributes to the overall understanding and learning of the subject. 

Ensure that the information you provide is sourced strictly from the given text chunk - do not introduce information that isn't present in the original text. The output should be organized in the following structure:

``` 
[
  {{
    "completeness": "<yes/no>",
    "chapter_title": "<Chapter Title>",
    "key_concepts": "<Key Concepts in the Chapter>",
    "chapter_contribution": "<Contribution of the Chapter towards the Subject>"
  }},
  .... (additional titles as identified)
]
``` 
The list contains all the individual chapters identified. 

Please ensure the output adheres to the provided format.

1. **Analyze the Text Chunk**: Begin by thoroughly reading the provided text chunk. This step requires you to comprehend and discern the significant themes or topics discussed in the text chunk.

2. During the analysis, it is crucial that you carefully evaluate each distinct discussion within the text chunk. Every section or topic area containing unique information should be assigned an appropriate title. 

3. Moreover, if a section presents multiple key points that can stand alone, it must be split into sub-sections, each with its own title. Remember, a chapter or sub-chapter should encapsulate a single coherent theme or main idea. 

4. Retain adherence to the original information flow and avoid over-segmentation of the details into disjointed parts. Ultimately, the aim is to deliver comprehensive comprehension of the text chunk, enriched by detailed identification of primary concepts and their contribution to the overall subject.

5. **Assess Chapter Completeness**: Evaluate the completeness of the chapter by ensuring it presents a comprehensive and coherent understanding of the topic. A complete chapter usually possesses a well-defined introduction, body, and conclusion.

6. **Identify Chapter Titles**: Upon understanding the main topics of the text chunk, assign titles to each chapter that genuinely encompass their core topics.

7. **Pinpoint Key Concepts**: Identify the critical ideas, theories, or notions within the text chunk that encapsulates the primary essence of the chapters. Such key points often connect the chapter content and offer a proper line of understanding.

8. **Evaluate Chapter Contribution**: Examine the chapter's contribution to the overall understanding and learning of the subject matter. This involves evaluating the unique insights or values the chapter adds to the broader subject. The contribution should be concise, precise, and not overly detailed and dont make it generic be specific.

9. **Formulate Precise Chapter Titles**: Ensure that the chapter titles succinctly reflect the main ideas of the chapters. Avoid using overly common or generic words in the titles for clarity.

10. **Create Apt Number of Chapters**: Group the subtopics appropriately into chapters to ensure coherent grasping of the subject matter. Avoid creating an excess number of chapters.

11. **Include Completeness Filter**: Each chapter's analysis should include a completion status – whether it is complete or incomplete.

The format for output is:

```
[
  {{
    "completeness": "<yes/no>",
    "chapter_title": "<Chapter Title>",
    "key_concepts": "<Key Concepts in the Chapter>",
    "chapter_contribution": "<Contribution of the Chapter towards the Subject>"
  }},
  .... (additional titles as identified)
]
```

The key objective of this process is not to segregate the chapter into standalone topics, but to comprehend the chapter holistically, summarising it accurately in terms of its key concepts and overall contribution to the subject matter. Most importantly, follow the specific output structure mentioned above without fail.

Input:
{input}"""


prompt_for_playbook = """Based on the provided chapter title, key concepts, chapter contribution, and the selected content, generate a playbook following a standard template structure. The playbook must include detailed explanations of key concepts using simple language, provide clear definitions, and utilize relevant examples from the content provided. Do not add any additional content outside of the provided material. Once the playbook is complete, ensure to proofread for coherence, grammatical accuracy, and alignment with the original content. The aim is to create a user-friendly guide for students that faithfully represents the original chapter content.

Instructions:

1. **Review the Material:** Begin by thoroughly analyzing the chapter title, key concepts, chapter contribution, and the provided content. Identify the significant themes and crucial information related to your specified chapter title.

2. **Follow a Standardized Template:** Use a consistent format every time you create a playbook. The basic structure should be: a clear topic heading, followed by definitions, key points, and relevant examples. 

3. **Indentify Relevant Content:** From the material given, discern the content that is specifically related to your chapter title. Ensure there is an alignment with the chapter title, key concepts, and the chapter's role.

4. **Set the Chapter Title:** Start the playbook with the provided chapter title as your topic. Keep the title clear and concise to reflect what the chapter will cover.

5. **Example and Definitions:** Follow the topic with definitions of the key concepts, as pulled directly from the provided content. Give clear, simple definitions for technical terms. Then add examples related to each concept, again focusing on simplicity and easy understanding.

6. **Elaborate on Key Concepts:** Leveraging the original content, provide a detailed explanation of each key concept in an easy-to-understand manner. Stick to the content provided.

7. **Highlight Chapter Contributions:** After the elaboration of each key concept, use the provided content to show how this chapter contributes to the overall subject matter. Ensure that the contribution is easy to comprehend, and resonates with the learner on why learning this chapter is significant.

8. **Restrict to Provided Content:** Don’t add any content or examples that weren’t part of the original material. The aim is to create a truthful representation of the chapter based on the provided content.

9. **Review and Edit:** Proofread the playbook to ensure all content flows seamlessly and there are no grammatical or typographic errors. Make sure all key concepts, definitions, contributions, and examples align with the provided material.

10. **Incorporate Formulas and Equations:** If the content provided includes any formulas or equations, ensure to incorporate these into the playbook. Represent each formula or equation in an understandable manner, providing a clear explanation of what each component of the formula or equation stands for. 

11. **Explain Complex Terms:** Should the content include technical or complex terms that may be difficult for students to comprehend, ensure to define these terms in a simple and clear language. For instance, if the term 'torque' is used, explain what it means in the simplest possible manner to promote a clear understanding.

By strictly adhering to these instructions, content will be generated solely based on the provided key concepts hence maintaining the integrity of your source material.

Chatper title: {chapter_title}
key Concepts: {key_concepts}
Chapter Contribution: {chapter_contribution}
Content: {content}"""


# Assuming the FilePath and FileName, DirectoryName classes are defined as provided in your question
class FileName(Enum):
    """File names."""

    DOCUMENT = "document.pkl"
    OUTPUT = "output.json"
    IMAGES = "images.json"
    LLAVA_OUTPUT = "llava_output.json"


class DirectoryName(Enum):
    """Directory names."""

    IMAGES = "images"
    OUTPUT = "output"
    SRC = "src"
    STORAGE = "storage"
    PLOTS = "plots"


# TODO: Add this to BaseModel
class FilePath():
    """File path.

    Args:
        file_path: the file path.
    """

    file_path: str = Field(description="The file path.")
    filename: str
    # def __str__(self) -> str:
    #     return self._filename

    def __init__(
        self,
        file_path: str,
    ):
        super().__init__()
        self.set_file_path(file_path)

    def set_file_path(self, file_path: str):
        """Set the file path."""
        self.file_path = file_path
        self.filename = file_path.split("/")[-1].split(".")[0]

    def _get_output_basedir_path(self) -> str:
        """Get the output path."""
        if not os.path.exists("output"):
            os.makedirs("output")

        basedir = f"output/{self.filename}"
        if not os.path.exists(basedir):
            os.makedirs(basedir)

        return basedir

    def get_storage_dir_path(self) -> str:
        """Get the storage path."""
        if not os.path.exists("storage"):
            os.makedirs("storage")

        return f"storage/{self.filename}"

    def get_output_file_path(self, file_name: FileName) -> str:
        """Get the output path."""
        return f"{self._get_output_basedir_path()}/{file_name.value}"

    def get_output_dir_path(self, dir_name: DirectoryName) -> str:
        """Get the output path."""
        output_dir = f"{self._get_output_basedir_path()}/{dir_name.value}"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        return output_dir


def parse_pdf(file_path):
    # Initialize the parser
    parser = LlamaParse(
        api_key="<LLAMA_PARSER_KEY>",
        result_type="text",
        num_workers=4,
        verbose=True,
        language="en",
    )
    
    # Get the relevant information
    document_filepath = file_path.get_output_file_path(FileName.DOCUMENT)
    if os.path.exists(document_filepath):
        with open(document_filepath, "rb") as f:
            documents = pickle.load(f)
    else:
        documents = parser.load_data(file_path=file_path.file_path)
        with open(document_filepath, "wb") as f:
            pickle.dump(documents, f)
    # st.write(f"document_filepath: {document_filepath}")
    # st.write(f"documents: {documents}")
    # Get the parsed data in JSON format
    json_output_filepath = file_path.get_output_file_path(FileName.OUTPUT)
    if os.path.exists(json_output_filepath):
        with open(json_output_filepath, "r") as f:
            json_objs = json.load(f)
    else:
        json_objs = parser.get_json_result(file_path=file_path.file_path)
        with open(json_output_filepath, "w") as f:
            json.dump(json_objs, f)

    # st.write(f"json_output_filepath: {json_output_filepath}")
    # st.write(f"json_objs: {json_objs}")

    pages = json_objs[0]['pages']

    # Get the images
    json_images_filepath = file_path.get_output_file_path(FileName.IMAGES)
    if os.path.exists(json_images_filepath):
        with open(json_images_filepath, "r") as f:
            images_dict = json.load(f)
    else:
        images_dict = parser.get_images(
            json_objs, download_path=file_path.get_output_dir_path(DirectoryName.IMAGES))
        with open(json_images_filepath, "w") as f:
            json.dump(images_dict, f)

    return documents, pages, images_dict

def user_message_generator(message):
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
            model="tiiuae/falcon-180b-chat",
        )
        return response.choices[0].message.content
       
    except Exception as e:
        return e


def main():
    st.title("Chapter Discovery")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    if uploaded_file is not None:
        # Save the uploaded file to a temporary file to process
        with open(uploaded_file.name, "wb") as f:
            f.write(uploaded_file.getbuffer())
        # st.write(f"uploaded_file.name: {uploaded_file.name}")
        file_path = FilePath(file_path=uploaded_file.name)
        # st.write(f"file_path: {file_path}")
        if st.button('Process Content'):
            with st.spinner('Processing...'):
                output = parse_pdf(file_path)
                all_data = '\n\n'.join([out.text for out in output[0]])
                
                # documents, pages, images_dict = output
                st.success('Processing complete!')

                st.subheader("Content Identified")
                st.write(all_data)
                
            with st.spinner('Identifying Chapters...'):
                output = prompt_for_chapter.format(input=all_data)
                output = user_message_generator(output)
                output = json.loads(output)
                st.subheader("Chapters Identified")
                st.json(output)
                
            with st.spinner('Discovering Playbook Chapters...'):
                for idx, out in enumerate(output):
                    st.markdown("---")
                    playbook_prompt = prompt_for_playbook.format(chapter_title=out["chapter_title"], key_concepts=out["key_concepts"],
                                                        chapter_contribution=out["chapter_contribution"], content=all_data)
                    playbook = user_message_generator(playbook_prompt)
                    st.subheader(f"Playbook {idx}")
                    st.markdown(playbook)
                    st.markdown("---")


if __name__ == "__main__":
    main()
