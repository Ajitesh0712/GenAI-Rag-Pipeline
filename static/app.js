let currentChatId = null;
window.sendMessage = async function() {

    const input =
        document.getElementById(
            "messageInput"
        );

    const chatBox =
        document.getElementById(
            "chatBox"
        );

    const message =
        input.value.trim();

    if (!message) {
        return;
    }

    chatBox.innerHTML += `

    <div class="message user-message">

        <div class="message-content">

            ${message}

        </div>

    </div>

    `;

    input.value = "";

    const response =
        await fetch(
            "/chat-stream",
            {
                method: "POST",
                headers: {
                    "Content-Type":
                        "application/json"
                },
                body: JSON.stringify({

                    chat_id: currentChatId,

                    message: message

                })
            }
        );

    const reader = response.body.getReader();

        const decoder = new TextDecoder();

        let answer = "";

        const assistantMessage = document.createElement("div");

        assistantMessage.className = "message assistant-message";

        assistantMessage.innerHTML = `

        <div class="message-content">

            <div class="assistant-title">

                <div class="assistant-avatar">

                    <i class="bi bi-stars"></i>

                </div>

                AI Assistant

            </div>

            <div class="streaming-answer mt-3"></div>

        </div>

        `;

        chatBox.appendChild(
            assistantMessage
        );

const answerDiv =
    assistantMessage.querySelector(
        ".streaming-answer"
    );
        let buffer = "";

        while (true) {

            const { done, value } =
                await reader.read();

            if (done) {
                break;
            }

            buffer += decoder.decode(
                value,
                {
                    stream: true
                }
            );

            const lines = buffer.split("\n");

            buffer = lines.pop();

            for (const line of lines) {

                if (!line.trim()) {
                    continue;
                }

                const event = JSON.parse(line);

                if (event.type === "token") {

                    answer += event.content;

                    answerDiv.innerHTML =
                        marked.parse(answer);

                }

                else if (event.type === "sources") {

                    let sourcesHTML = `

                        <div class="sources">

                            <strong>📄 Sources</strong><br>

                    `;

                    event.content.forEach(source => {

                        sourcesHTML += `

                            <span class="source-chip">

                                ${source.filename}

                            </span>

                        `;

                    });

                    sourcesHTML += "</div>";

                    answerDiv.innerHTML += sourcesHTML;

                }

                else if (event.type === "done") {

                    console.log("Streaming Finished");

                    await window.loadChats();

                }

                chatBox.scrollTop =
                    chatBox.scrollHeight;

            }

        }
    }

window.uploadDocument = async function() {
    
    const fileInput =
        document.getElementById(
            "fileInput"
        );

    if (
        fileInput.files.length === 0
    ) {
        alert("Select a file");
        return;
    }

    const formData =
        new FormData();

    formData.append(
        "file",
        fileInput.files[0]
    );

    const response =
        await fetch(
            "/upload",
            {
                method: "POST",
                body: formData
            }
        );

    const data =
        await response.json();

    if (!response.ok) {

        alert(data.detail);

        return;

    }

    document.getElementById(
        "uploadStatus"
    ).innerHTML =
        `Indexed ${data.chunks} chunks from ${data.filename}`;
        await window.loadDocuments();
}



window.loadDocuments = async function () {

    const response = await fetch("/documents");

    const data = await response.json();

    const container =
        document.getElementById("documentsList");

    container.innerHTML = "";
    document.getElementById(
        "knowledgeCount"
    ).textContent =
        `(${data.documents.length})`;

    data.documents.forEach(doc => {

        let badge = "PDF";
        let badgeClass = "badge-pdf";

        let displayName = doc.filename;

        if (doc.filename.startsWith("http")) {

            badge = "URL";
            badgeClass = "badge-url";

            const url = new URL(doc.filename);

            const parts = url.pathname.split("/");

            displayName = decodeURIComponent(
                parts[parts.length - 1]
            );

            displayName = displayName.replace(/_/g, " ");

        }

        container.innerHTML += `

            <div class="document-card">

                <button
                    class="delete-btn"
                    onclick="window.deleteDocument('${doc.filename}')">

                    <i class="bi bi-trash"></i>

                </button>

                <div class="document-title">

                    <span class="document-name">

                        ${displayName}

                    </span>

                    <span class="source-badge ${badgeClass}">

                        ${badge}

                    </span>

                </div>

                <div class="document-info">

                    ${doc.chunks} Chunks

                </div>

            </div>

        `;

    });

}
window.loadChats = async function(){

    const response =
        await fetch("/chats");

    const data =
        await response.json();

    const container =
        document.getElementById("chatList");

    container.innerHTML = "";

    data.chats.forEach(chat=>{

        container.innerHTML += `

            <div
                class="chat-card">

                <span
                    class="chat-title"
                    onclick="window.openChat(${chat.id})">

                    💬 ${chat.title}

                </span>

                <button
                    class="delete-chat-btn"
                    onclick="event.stopPropagation(); window.deleteChat(${chat.id})">

                    <i class="bi bi-trash"></i>

                </button>

            </div>

        `;

    });

}
window.openChat = async function(chatId){

    currentChatId = chatId;

    const response =
        await fetch(`/chat/${chatId}`);

    const data =
        await response.json();

    const chatBox =
        document.getElementById("chatBox");

    chatBox.innerHTML = "";

    data.messages.forEach(message=>{

        if(message.role==="user"){

            chatBox.innerHTML += `

                <div class="message user-message">

                    <div class="message-content">

                        ${message.content}

                    </div>

                </div>

            `;

        }

        else{

            chatBox.innerHTML += `

                <div class="message assistant-message">

                    <div class="message-content">

                        <div class="assistant-title">

                            <div class="assistant-avatar">

                                <i class="bi bi-stars"></i>

                            </div>

                            AI Assistant

                        </div>

                        <div class="mt-3">

                            ${marked.parse(message.content)}

                        </div>

                    </div>

                </div>

            `;

        }

    });

    chatBox.scrollTop =
        chatBox.scrollHeight;

}

window.onload = function () {

    window.loadDocuments();
    window.loadChats();

}

window.deleteDocument = async function (filename) {

    const confirmDelete = confirm(
        `Delete "${filename}" ?`
    );

    if (!confirmDelete) {
        return;
    }

    const response = await fetch(

        `/documents/${encodeURIComponent(filename)}`,

        {
            method: "DELETE"
        }

    );

    const data = await response.json();

    if (data.success) {

        alert(
            `Deleted ${data.deleted_chunks} chunks`
        );

        await window.loadDocuments();

    }
}

document.getElementById("fileInput").addEventListener("change", function(){

    const label = document.getElementById("selectedFile");

    if(this.files.length){

        label.textContent = this.files[0].name;

    }else{

        label.textContent = "No file selected";

    }

});

window.uploadURL = async function () {

    const input =
        document.getElementById("urlInput");

    const url = input.value.trim();

    if (!url) {

        alert("Please enter a URL");

        return;

    }

    const response = await fetch("/upload-url", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            url: url
        })

    });

    const data = await response.json();

    if (!response.ok) {

        alert(data.detail);

        return;

    }

    document.getElementById("uploadStatus").innerHTML =
        `Indexed ${data.chunks} chunks`;

    input.value = "";

    await window.loadDocuments();

}

document
    .getElementById("newChatBtn")
    .addEventListener(
        "click",
        async function () {

            await fetch(
                "/chat/reset",
                {
                    method: "POST"
                }
            );

            const response = await fetch(
                "/chat/new",
                {
                    method: "POST"
                }
            );

            const data = await response.json();

            currentChatId = data.chat_id;

            document.getElementById(
                "chatBox"
            ).innerHTML = "";

            await window.loadChats();

        }
    );


const modal =
    document.getElementById(
        "knowledgeModal"
    );

document
.getElementById("addKnowledgeBtn")
.onclick=function(){

    modal.style.display="flex";

};

document
.getElementById("closeModal")
.onclick=function(){

    modal.style.display="none";

};

const knowledgeHeader =
    document.getElementById("knowledgeHeader");

const knowledgeList =
    document.getElementById("documentsList");

const knowledgeArrow =
    document.getElementById("knowledgeArrow");

knowledgeHeader.onclick = function(){

    if(knowledgeList.style.display==="none"){

        knowledgeList.style.display="block";

        knowledgeArrow.className =
            "bi bi-chevron-down";

    }

    else{

        knowledgeList.style.display="none";

        knowledgeArrow.className =
            "bi bi-chevron-right";

    }

}

window.deleteChat = async function(chatId){

    const confirmDelete = confirm(
        "Delete this chat?"
    );

    if(!confirmDelete){
        return;
    }

    const response = await fetch(

        `/chat/${chatId}`,

        {
            method:"DELETE"
        }

    );

    const data =
        await response.json();

    if(data.success){

        await window.loadChats();

        document.getElementById(
            "chatBox"
        ).innerHTML = "";

    }

}