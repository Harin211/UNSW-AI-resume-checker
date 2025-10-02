# UNSW AI Resume Analyzer  

An AI-powered web app that recommends **UNSW electives based on your resume**.  
Upload your resume PDF, and get a ranked list of courses that align with your skills and interests.  

---

## Features  
- **Upload your resume (PDF)** directly through the web interface  
- **AI-powered analysis** extracts skills and experiences from the resume  
- **Smart course recommendations** matched against UNSW course data 
- **Cross-device support**: works across different machines/networks using **FastAPI + ngrok**  
-  **Modern UI** built with Jinja2 templates and FastAPI  

---

## Tech Stack  
- **Backend**: FastAPI, httpx  
- **Text Extraction**: PyMuPDF (`fitz`)  
- **AI Model**: Custom-trained model on course dataset + DevSoc API  
- **Frontend**: Jinja2 templates + HTML/CSS  
- **Networking**: ngrok for tunneling requests across networks  

---

## Live Demo
[web-production-92048.up.railway.app](https://web-production-92048.up.railway.app/)

