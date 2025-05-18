# aluraChallenge
Overview
The AI Social Impact Mentor is a Python-based application designed to empower users to address local social issues, such as food insecurity, lack of clean water, or educational disparities. Built with the Textual framework and powered by the Gemini API, this tool guides users in creating actionable plans, connects them with nearby NGOs, and provides motivational feedback to sustain engagement. Inspired by community-driven initiatives like the Disaster Response Coordinator and advocacy-focused AI Community Storyteller, it tackles Brazil’s social inequalities by fostering grassroots change.

Problem Statement
Social challenges, like 33 million Brazilians lacking access to clean water or 60% of income concentrated among the top 10%, demand community-driven solutions. Individuals often feel overwhelmed or unsure where to start. The AI Social Impact Mentor bridges this gap by offering tailored action plans, local resources, and encouragement, empowering users to make a tangible difference in their communities.

Features
Input Form: Users specify a social issue (e.g., "food insecurity in São Paulo"), budget (e.g., R$50), time available (e.g., 10 hours), location, and progress stage (initial, in progress, or stalled).
Action Plan: Generates a 4–6 step actionable plan in markdown, tailored to the user’s inputs (e.g., "Contact local food banks, organize a community drive").
NGO Suggestions: Recommends nearby NGOs with details like name, distance, contact, and mission, using a fallback dataset or Gemini API for real-time suggestions.
Motivational Feedback: Provides personalized encouragement based on the user’s progress (e.g., "Your efforts can transform lives in Rio!").
Interactive Interface: Built with Textual, offering a clean, terminal-based UI with input fields, buttons, and dynamic output.
Tech Stack
Python: Core language for logic and API integration.
Textual: Framework for building an interactive terminal UI.
Gemini API: Powers text generation for plans, NGO suggestions, and motivational messages.
Fallback Data: Hardcoded NGO dataset ensures functionality if API access is limited.
Asyncio: Handles asynchronous API calls for smooth performance.
How It Works
Users input their social issue, budget, time, location, and progress via a Textual interface.
The app processes inputs using the Gemini API to:
Summarize the plan in markdown.
Break it into actionable steps.
Estimate costs within the budget.
Suggest relevant NGOs.
Generate motivational messages.
Results are displayed in a single, formatted output in the UI.
Example Prompt
You are an AI social impact mentor. A user wants to address food insecurity in São Paulo with R$50 and 10 hours. Generate a 5-step plan, suggest 2 NGOs, and provide motivational feedback. Output in markdown.

Sample Output:

markdown

Copy
### Resumo do Plano
Combater a insegurança alimentar em São Paulo com R$50 e 10 horas.

### Plano de Ação
1. Pesquisar cozinhas comunitárias locais (2h).
2. Comprar alimentos não perecíveis (R$30, 1h).
3. Doar para uma ONG local (1h).
4. Divulgar a causa nas redes sociais (3h).
5. Planejar uma arrecadação comunitária (3h).

### Estimativa de Custos
- Alimentos: R$30
- Transporte: R$10
- Materiais de divulgação: R$10

### ONGs Sugeridas
- **Fundo Água São Paulo**: 5km, contato@spagua.org, missão: Acesso à água potável.
- **Comida para Todos SP**: 3km, info@comidaparatodos.org, missão: Combater a fome.

### Mensagem Motivacional
Sua iniciativa pode alimentar famílias em São Paulo! Cada passo conta.
Installation
Clone the repository:
bash

Copy
git clone https://github.com/yourusername/ai-social-impact-mentor.git
cd ai-social-impact-mentor
Install dependencies:
bash

Copy
pip install textual google-generativeai
Set up the Gemini API key:
Replace "AIzaSyANuWDVQs8CHuSfnpOY0mZYYrBrW3bECHQ" in the code with your own key.
Run the app:
bash

Copy
python main.py
Why It Matters
This project aligns with the mission to address problemas sociais by empowering communities to tackle issues like poverty, hunger, and environmental challenges. It promotes educação through advocacy training and accessible tools, making social impact achievable for anyone. Its creative use of AI and focus on local solutions mirror the innovative spirit of Alura’s 2025 curriculum.

Future Improvements
Integrate Google Places API or web scraping for real-time NGO data.
Add multilingual support for broader accessibility.
Incorporate a progress tracker to log user actions and milestones.
Demo
Screenshots: See the Textual UI in action with sample inputs and outputs (to be added).
Video Demo: A walkthrough of creating a plan for addressing food insecurity (planned).
Colab Notebook: Prototype available for testing the Gemini API integration (optional).
Contributing
Contributions are welcome! Please open an issue or submit a pull request for bug fixes, new features, or improvements.

Acknowledgments
Inspired by Alura’s 2024 winners, MedGrandma-AI and Disaster Response Coordinator, for their focus on accessibility and community impact.
