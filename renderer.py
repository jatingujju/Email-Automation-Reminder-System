from jinja2 import Environment, FileSystemLoader
import markdown


class EmailRenderer:

    def __init__(self, template_dir="templates"):

        self.env = Environment(
            loader=FileSystemLoader(template_dir)
        )

    def render_markdown_template(self, template_name, context):

        # Load markdown template
        template = self.env.get_template(template_name)

        # Merge template with context
        rendered_markdown = template.render(context)

        # Convert markdown to HTML
        rendered_html = markdown.markdown(rendered_markdown)

        return rendered_html


if __name__ == "__main__":

    renderer = EmailRenderer()

    sample_context = {
        "name": "Rahul Sharma",
        "event_name": "Interview Session",
        "event_date": "10 May 2026",
        "event_time": "10:00 AM"
    }

    html_output = renderer.render_markdown_template(
        "reminder.md",
        sample_context
    )

    print(html_output)