import base64
import os
import io
import pdf2image
import google.generativeai as genai

# Set the Google API key using an environment variable for security
os.environ["GOOGLE_API_KEY"] = ""
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the first page of the PDF to an image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        # Convert image to byte array for base64 encoding
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Prepare the image in base64 format for API use
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Define a prompt for the Generative AI model
input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Provide the match percentage if the resume matches
the job description. Output should include the percentage match first, followed by missing keywords, and finally, overall feedback.
"""

# Example job description text
input_text = '''
Responsibilities:

Develop and optimise machine learning models for natural language processing (NLP) and computer vision tasks.
Lead the building of data pipelines and ETL processes to manage and process large datasets.
Collaborate with cross-functional teams to create moderation pipelines for our platform, ensuring safe and secure user experiences.
Implement real-time monitoring and debugging systems to ensure high performance and scalability.
Work on adding new features and expanding the moderation capabilities of the platform.


Requirements:

MUST have experience with natural language processing (NLP)
MUST have experience with computer vision processing
MUST have experience building data pipelines and ETL processes
MUST be based in London or willing to relocate (relocation packages available)
Ideally has experience with building moderation pipelines
Ideally has AWS experience
Small plus if crypto native

'''

# Placeholder for uploaded file content
# Replace 'sample.pdf' with the path to your test PDF file or pass an uploaded file object in a real setup
with open("test-cv.pdf", "rb") as uploaded_file:
    pdf_content = input_pdf_setup(uploaded_file)

# Get response from Generative AI model
response = get_gemini_response(input_prompt3, pdf_content, input_text)

print(response)
