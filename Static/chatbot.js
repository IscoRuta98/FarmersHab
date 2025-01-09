function toggleChatbot() {
    const chatbotWindow = document.getElementById("chatbot-window");
    chatbotWindow.classList.toggle("hidden");
    chatbotWindow.style.display = chatbotWindow.style.display === "none" ? "flex" : "none";
}

function sendMessage() {
    const input = document.getElementById("chatbot-input");
    const message = input.value.trim();
    const messagesContainer = document.getElementById("chatbot-messages");

    if (message) {
        const userMessage = document.createElement("p");
        userMessage.innerHTML = `<strong>You:</strong> ${message}`;
        messagesContainer.appendChild(userMessage);

        const response = getChatbotResponse(message);
        const botMessage = document.createElement("p");
        botMessage.innerHTML = `<strong>Chatbot:</strong> ${response}`;
        messagesContainer.appendChild(botMessage);

        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        input.value = "";
    }
}

function getChatbotResponse(message) {
    const responses = {
        "how to grow maize": "To grow maize, prepare the soil, plant seeds in rows, and water regularly. Ensure the soil has adequate nitrogen.",
        "what is the best fertilizer": "Use phosphorus-rich fertilizer to promote root growth and higher yield.",
        "how to apply for loans": "Visit the CEDA website or your nearest office to start the loan application process."
    };

    return responses[message.toLowerCase()] || "I'm sorry, I don't have an answer for that.";
}

