# ConsciencIA - AI Social Impact Mentor

#### Overview
The **AI Social Impact Mentor** is a Python-based application designed to empower users to address local social issues, such as food insecurity, lack of clean water, or educational disparities. Built with the Textual framework and powered by the Gemini API, this tool guides users in creating actionable plans, connects them with nearby NGOs, and provides motivational feedback to sustain engagement. Inspired by community-driven initiatives like the *Disaster Response Coordinator* and advocacy-focused *AI Community Storyteller*, it tackles Brazil’s social inequalities by fostering grassroots change.

#### Problem Statement
Social challenges, like 33 million Brazilians lacking access to clean water or 60% of income concentrated among the top 10%, demand community-driven solutions. Individuals often feel overwhelmed or unsure where to start. The AI Social Impact Mentor bridges this gap by offering tailored action plans, local resources, and encouragement, empowering users to make a tangible difference in their communities.

#### Features
1. **Input Form**: Users specify a social issue (e.g., "food insecurity in São Paulo"), budget (e.g., R$50), time available (e.g., 10 hours), location, and progress stage (initial, in progress, or stalled).
2. **Action Plan**: Generates a 4–6 step actionable plan in markdown, tailored to the user’s inputs (e.g., "Contact local food banks, organize a community drive").
3. **NGO Suggestions**: Recommends nearby NGOs with details like name, distance, contact, and mission, using a fallback dataset or Gemini API for real-time suggestions.
4. **Motivational Feedback**: Provides personalized encouragement based on the user’s progress (e.g., "Your efforts can transform lives in Rio!").
5. **Interactive Interface**: Built with Textual, offering a clean, terminal-based UI with input fields, buttons, and dynamic output.

![image](https://github.com/user-attachments/assets/059a35e2-795b-4abe-bd36-521a12740bb0)

#### Tech Stack
- **Python**: Core language for logic and API integration.
- **Textual**: Framework for building an interactive terminal UI.
- **Gemini API**: Powers text generation for plans, NGO suggestions, and motivational messages.
- **Fallback Data**: Hardcoded NGO dataset ensures functionality if API access is limited.
- **Asyncio**: Handles asynchronous API calls for smooth performance.

#### How It Works
1. Users input their social issue, budget, time, location, and progress via a Textual interface.
2. The app processes inputs using the Gemini API to:
   - Summarize the plan in markdown.
   - Break it into actionable steps.
   - Estimate costs within the budget.
   - Suggest relevant NGOs.
   - Generate motivational messages.
3. Results are displayed in a single, formatted output in the UI.

#### Example Prompt
> You are an AI social impact mentor. A user wants to address food insecurity in São Paulo with R$50 and 10 hours. Generate a 5-step plan, suggest 2 NGOs, and provide motivational feedback. Output in markdown.

**Sample Output**:
```markdown
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
```

#### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/JosueMonteiroUchoaAlves/aluraChallenge.git
   cd aluraChallenge
   ```
2. Install dependencies:
   ```bash
   pip install textual google-generativeai
   ```
3. Set up the Gemini API key:
   - Replace `"YOUR_API_KEY"` in the code with your own key.
4. Run the app:
   ```bash
   python main.py
   ```

#### Why It Matters
This project aligns with the mission to address *problemas sociais* by empowering communities to tackle issues like poverty, hunger, and environmental challenges. It promotes *educação* through advocacy training and accessible tools, making social impact achievable for anyone. Its creative use of AI and focus on local solutions mirror the innovative spirit of Alura’s 2025 curriculum.

#### Future Improvements
- Integrate Google Places API or web scraping for real-time NGO data.
- Add multilingual support for broader accessibility.
- Incorporate a progress tracker to log user actions and milestones.

#### Contributing
Contributions are welcome! After May 19, please open an issue or submit a pull request for bug fixes, new features, or improvements.

#### Acknowledgments
Inspired by Alura’s 2024 winners, *MedGrandma-AI* and *Disaster Response Coordinator*, for their focus on accessibility and community impact.
