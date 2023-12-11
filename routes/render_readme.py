""" Simple route for displaying the README.md file """
import markdown
from routes import doc


@doc.route('/')
def render_readme():
    """ Render a README.md file for user convenience """

    # Read the content of the README.md file
    with open('README.md', 'r', encoding='utf-8') as readme_file:
        readme_content = readme_file.read()

    # Convert markdown to HTML
    html_content = markdown.markdown(readme_content)

    # Return the html content
    return html_content
