$(document).ready(function () {
    const chatWindow = $('#chat-window');
    const messageList = $('#message-list');
    const messageInput = $('#message-input');
    const sendButton = $('#send-button');
    const targetLangSelect = $('#target-lang-select');
    const loadingAnimation = $('.my-loading');

    let isRecording = false;
    let mediaRecorder;
    let audioChunks = [];

    function appendMessage(role, text) {
        const label = role === 'user' ? 'USER_INPUT' : 'AI_TRANSLATION';
        const msgHtml = `
            <div class="msg-container mb-4">
                <div class="msg-label text-uppercase mb-1">${label}</div>
                <div class="msg-text ${role === 'user' ? 'user-msg' : 'bot-msg'}">
                    ${text}
                </div>
            </div>`;
        
        messageList.append(msgHtml);
        
        chatWindow.animate({
            scrollTop: chatWindow[0].scrollHeight
        }, 300);
    }

    async function translateText(text) {
        const targetLang = targetLangSelect.val();
        loadingAnimation.removeClass('d-none');

        try {
            const response = await fetch('/process-message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    userMessage: text,
                    targetLang: targetLang
                })
            });

            const data = await response.json();
            
            appendMessage('bot', data.openaiResponseText);

            if (data.openaiResponseSpeech) {
                const audio = new Audio("data:audio/wav;base64," + data.openaiResponseSpeech);
                audio.play();
            }
        } catch (error) {
            console.error("Erreur serveur:", error);
            appendMessage('bot', "ERR_SYSTEM: Impossible de joindre le service de traduction.");
        } finally {
            loadingAnimation.addClass('d-none');
        }
    }

    // --- GESTION DES ENTRÉES CLAVIER ---
    messageInput.on('keypress', function (e) {
        if (e.which === 13 && messageInput.val().trim() !== "") {
            const text = messageInput.val();
            appendMessage('user', text);
            translateText(text);
            messageInput.val('');
        }
    });

    // --- GESTION DES ENTRÉES VOCALES ---
    sendButton.on('click', async function () {
        if (!isRecording) {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);
                audioChunks = [];

                mediaRecorder.ondataavailable = (event) => audioChunks.push(event.data);
                
                mediaRecorder.onstop = async () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    loadingAnimation.removeClass('d-none');

                    const response = await fetch('/speech-to-text', {
                        method: 'POST',
                        body: audioBlob
                    });
                    const data = await response.json();

                    if (data.text && data.text !== 'null' && data.text.trim() !== "") {
                        appendMessage('user', data.text);
                        translateText(data.text);
                    } else {
                        loadingAnimation.addClass('d-none');
                        console.warn("Audio non reconnu ou vide.");
                    }
                };

                mediaRecorder.start();
                isRecording = true;

                $(this).addClass('active btn-danger')
                       .html('<i class="fa fa-stop mr-2"></i> STOP');
                
            } catch (err) {
                alert("Erreur d'accès au microphone : " + err);
            }
        } else {
            mediaRecorder.stop();
            isRecording = false;

            $(this).removeClass('active btn-danger')
                   .html('<i class="fa fa-microphone mr-2"></i> RECORD');
        }
    });
});