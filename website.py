import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Hackathon Project",
    page_icon="🚀",
    layout="wide"
)

# Title and subtitle
st.title("Welcome to Our Hackathon Project! 🚀")
st.subheader("Innovating Solutions for a Better Future")

# Replace placeholders with real content

# About the project
st.header("About the Project")
st.write("""
Our project was developed during the Global Hackathon 2025 to address the challenge of food waste. 
We aim to create a platform that connects surplus food providers with those in need, reducing waste and hunger. 
This website provides an overview of our solution, its features, and the impact it can create.
""")

# Team introduction
st.header("Meet the Team")
st.write("""
We are a group of passionate individuals with diverse skills, working together to bring this project to life:
- **Alice Johnson**: Data Scientist
- **Bob Smith**: Full-Stack Developer
- **Charlie Lee**: UX Designer
- **Dana White**: Project Manager
""")

# Features of the project
st.header("Key Features")
st.write("""
Here are the main features of our project:
1. **Real-Time Food Matching**: Matches surplus food with nearby recipients.
2. **Analytics Dashboard**: Provides insights into food waste reduction.
3. **Mobile-Friendly Interface**: Accessible on any device.
""")

# Demo section
st.header("Live Demo")
st.write("Check out our project in action below:")

# Add functionality to the button
if st.button("Run Demo"):
    st.write("The demo is running! 🚀")
    # Add your demo logic here
    # For example, call a function or display additional content
    st.write("This is where the demo output will appear.")

# Contact information
st.header("Get in Touch")
st.write("""
If you'd like to learn more about our project or collaborate with us, feel free to reach out:
- **Email**: [your_email@example.com]
- **GitHub**: [GitHub Repository Link]
- **LinkedIn**: [LinkedIn Profile Link]
""")

# Footer
st.markdown("---")
st.write("Thank you for visiting our project website! We hope you find it inspiring and impactful.")