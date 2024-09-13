# LinkedIn PDF to HTML Resume Converter (Streamlit Version)

This Streamlit web application converts a LinkedIn PDF download into an HTML resume. It simulates the use of an OpenAI API key input without actually using the API for functionality.

## How it works

1. The user uploads a LinkedIn PDF and provides a simulated OpenAI API key.
2. The application extracts text from the PDF using PyPDF2.
3. The extracted text is parsed to identify different sections of the LinkedIn profile.
4. An HTML resume is generated using a predefined template.
5. The generated HTML resume is presented for preview and download.

## Approach and Solution

1. **PDF Text Extraction**: We use PyPDF2 to extract text from the uploaded LinkedIn PDF.

2. **Text Parsing**: A custom parsing function (`parse_linkedin_text`) is implemented to identify different sections of the LinkedIn profile (name, title, about, experience, education, skills). This function may need to be adjusted based on the specific format of LinkedIn PDFs.

3. **HTML Generation**: We use a predefined HTML template to generate the resume. The parsed data is inserted into this template.

4. **Streamlit Web Application**: We use Streamlit to create a simple and interactive web interface for file upload, resume generation, and preview.

5. **Simulated API Key**: While we collect an API key from the user, it's not used in the actual functionality. This simulates the structure of an API-dependent application without the actual API usage.

## Deployment

This application can be easily deployed on Streamlit Sharing or other platforms that support Streamlit apps. The deployment process typically involves:

1. Pushing the code to a GitHub repository.
2. Connecting the repository to Streamlit Sharing.
3. Streamlit Sharing will automatically detect the requirements and deploy the app.

## Local Development

To run this application locally:

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the Streamlit application: `streamlit run app.py`
4. Open a web browser and navigate to the URL provided by Streamlit (typically `http://localhost:8501`)

## Future Improvements

- Enhance the PDF parsing to handle more complex LinkedIn profile structures.
- Add more customization options for the generated resume.
- Implement error handling and user feedback.

## License

This project is open source and available under the MIT License.
## Demo

Insert gif or link to demo

