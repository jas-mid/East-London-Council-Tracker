Summary:
The goal of the East London Council Comparison Application is to be a tool used to compare the performances of councils in East London. The application puts certain council-controlled metrics into perspective in relation to the Greater London average and other East London councils. It does this by graphically displaying the metrics as bar graphs within the frame of the largest value within the metric. The bar graph can be interacted with to see the specific values of each metric, and users can zoom in and out to see finer or broader details.

The goal of the app is to raise awareness among residents so that they know what their council needs to improve, since other councils in similar situations are performing better in the same metrics. It further provides the information and means on how you can reach out to your council and how you can get your voice heard in your local area. It does this by directing you to the contact us page of the council. It also provides information surrounding voting and connects the user to the voting registration page for each council.

To run the code:
1) Pip install all libraries below:
- pandas==2.3.3
- plotly==6.6.0
- pytest==9.0.2
- streamlit==1.53.1
- (if dependencies are not met, run "pip install -r requirements.txt")

2) In terminal, paste and run "streamlit run app.py"

3) Open browser to page that Streamlit opened




To-do List:
- Add pings to page links to ensure that they are active
- Implement APIs to get active data
- Improve layout and flow (more intuitive design)
- Make into webpage and host?
