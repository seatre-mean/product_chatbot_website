const chatbotPanel = document.getElementById("chatbot-panel");
const chatbotToggle = document.getElementById("chatbot-toggle");
const chatbotInput = document.getElementById("chatbot-input");
const chatbotMessages = document.getElementById("chatbot-messages");

function openChatbot() {
    chatbotPanel.style.display = "flex";
    chatbotToggle.style.display = "none";
    chatbotInput.focus();
}

function closeChatbot() {
    chatbotPanel.style.display = "none";
    chatbotToggle.style.display = "block";
}

function toggleChatbot() {
    if (chatbotPanel.style.display === "flex") {
        closeChatbot();
    } else {
        openChatbot();
    }
}

function addMessage(text, type, extraClass = "") {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${type}-message ${extraClass}`;
    messageDiv.textContent = text;

    chatbotMessages.appendChild(messageDiv);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;

    return messageDiv;
}

async function sendMessage(customMessage = null) {
    const message = customMessage || chatbotInput.value.trim();

    if (!message) {
        return;
    }

    openChatbot();

    addMessage(message, "user");
    chatbotInput.value = "";

    const loadingMessage = addMessage("Typing...", "bot", "loading");

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        loadingMessage.remove();

        addMessage(data.reply, "bot");

    } catch (error) {
        loadingMessage.remove();
        addMessage("Sorry, the chatbot is not available right now. Please try again later.", "bot");
    }
}

function askFromButton(question) {
    sendMessage(question);
}

chatbotInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});
