const chatForm = document.getElementById("chat-form");
const questionInput = document.getElementById("question-input");
const sendButton = document.getElementById("send-button");
const chatOutput = document.getElementById("chat-output");

const history = [];

function createThinkingElement() {
  const thinkingElement = document.createElement("p");
  thinkingElement.className = "thinking";
  thinkingElement.id = "thinking-indicator";
  thinkingElement.textContent = "IA pensando...";
  return thinkingElement;
}

function removeThinkingElement() {
  const thinkingElement = document.getElementById("thinking-indicator");
  if (thinkingElement) thinkingElement.remove();
}

function appendMessage(role, content, responseData) {
  const rowElement = document.createElement("article");
  rowElement.className = `message-row ${role}`;

  const avatarElement = document.createElement("div");
  avatarElement.className = "avatar";
  avatarElement.textContent = role === "user" ? "EU" : "IA";

  const messageElement = document.createElement("div");
  messageElement.className = `message ${role}`;

  const roleElement = document.createElement("p");
  roleElement.className = "message-role";
  roleElement.textContent = role === "user" ? "Voce" : "Assistente";

  const contentElement = document.createElement("p");
  contentElement.className = "message-content";
  contentElement.textContent = content;

  messageElement.append(roleElement, contentElement);

  if (role === "assistant" && responseData) {
    const sectionsWrapper = document.createElement("section");
    sectionsWrapper.className = "response-sections";

    responseData.sections.forEach((section) => {
      const sectionElement = document.createElement("div");
      sectionElement.className = "response-section";

      const title = document.createElement("h4");
      title.textContent = section.title;

      const sectionContent = document.createElement("p");
      sectionContent.className = "message-content";
      sectionContent.textContent = section.content;

      sectionElement.append(title, sectionContent);
      sectionsWrapper.appendChild(sectionElement);
    });

    const summaryElement = document.createElement("p");
    summaryElement.className = "response-summary";
    summaryElement.textContent = `Resumo: ${responseData.summary}`;

    messageElement.append(sectionsWrapper, summaryElement);
  }

  rowElement.append(avatarElement, messageElement);
  chatOutput.appendChild(rowElement);
  chatOutput.scrollTop = chatOutput.scrollHeight;
}

function setSendingState(isSending) {
  sendButton.disabled = isSending;
  questionInput.disabled = isSending;
  sendButton.textContent = isSending ? "Enviando..." : "Enviar";
}

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const question = questionInput.value.trim();
  if (!question) return;

  appendMessage("user", question);
  history.push({ role: "user", content: question });
  questionInput.value = "";
  setSendingState(true);
  chatOutput.appendChild(createThinkingElement());
  chatOutput.scrollTop = chatOutput.scrollHeight;

  try {
    const response = await fetch("/chat/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: question,
        history,
      }),
    });

    if (!response.ok) {
      throw new Error("Falha ao consultar o backend.");
    }

    const data = await response.json();
    const assistantSummary = data.response?.summary || "Sem resumo.";

    removeThinkingElement();
    appendMessage("assistant", assistantSummary, data.response);
    history.push({ role: "assistant", content: assistantSummary });
  } catch (error) {
    removeThinkingElement();
    appendMessage(
      "assistant",
      "Nao foi possivel obter resposta no momento. Tente novamente."
    );
    console.error(error);
  } finally {
    setSendingState(false);
    questionInput.focus();
  }
});

appendMessage(
  "assistant",
  "Oi! Me envie uma pergunta para comecarmos.",
  {
    sections: [
      {
        title: "Dica",
        content: "Voce pode perguntar sobre algoritmos, IA, backend, arquitetura ou qualquer tema de estudo.",
      },
    ],
    summary: "Estou pronto para te ajudar.",
  }
);
