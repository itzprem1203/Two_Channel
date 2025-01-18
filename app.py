import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QColor, QImageReader
from PyQt5.QtCore import Qt

class ImageToHtmlApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image to HTML & CSS")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        self.layout = QVBoxLayout()

        # Instructions
        self.instructions = QLabel("Click 'Select Image' to choose an image, and generate HTML & CSS.")
        self.layout.addWidget(self.instructions)

        # Button to select an image
        self.select_image_btn = QPushButton("Select Image")
        self.select_image_btn.clicked.connect(self.select_image)
        self.layout.addWidget(self.select_image_btn)

        # Text area to display the generated code
        self.code_area = QTextEdit()
        self.code_area.setReadOnly(True)
        self.layout.addWidget(self.code_area)

        # Set central widget
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def select_image(self):
        # Open file dialog to select image
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select an Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        
        if file_path:
            # Generate HTML and CSS code
            html_code, css_code = self.generate_html_css_from_image(file_path)
            
            # Display the code in the text area
            self.code_area.setPlainText(f"HTML Code:\n{html_code}\n\nCSS Code:\n{css_code}")

    def generate_html_css_from_image(self, file_path):
        # Here, you would process the image to generate HTML and CSS for its shapes and colors
        # For the sake of simplicity, let's assume we have a two-color image with rectangles

        # Manually defined colors (these could be derived from the image)
        primary_color = "#FF5733"  # Example color
        secondary_color = "#33FF57"  # Example color

        # Example HTML code with these colors
        html_code = f"""
<div class="container">
    <div class="rectangle primary"></div>
    <div class="circle secondary"></div>
</div>
"""

        # Example CSS code to style the shapes
        css_code = f"""
.container {{
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}}

.rectangle {{
    width: 200px;
    height: 100px;
    background-color: {primary_color};
    margin: 10px;
}}

.circle {{
    width: 100px;
    height: 100px;
    background-color: {secondary_color};
    border-radius: 50%;
    margin: 10px;
}}
"""

        return html_code, css_code

# Main execution
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageToHtmlApp()
    window.show()
    sys.exit(app.exec_())
