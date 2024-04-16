document.addEventListener('DOMContentLoaded', function() {
    fetchRandomCollectible();

    document.getElementById('guess-form').addEventListener('submit', function(event) {
        event.preventDefault();
        const guess = document.getElementById('guess').value.trim();
        const collectibleName = document.getElementById('collectible-name').innerText.trim();

        checkAnswer(guess, collectibleName);
    });
});

function fetchRandomCollectible() {
    fetch('/get_random_collectible')
        .then(response => response.json())
        .then(data => {
            document.getElementById('collectible-name').innerText = data.collectible[2];
            document.getElementById('hint').innerText = `Dica: ${data.hint}`;
        })
        .catch(error => console.error('Error fetching random collectible:', error));
}

function checkAnswer(guess, collectibleName) {
    const formData = {
        guess: guess,
        collectible_name: collectibleName
    };

    fetch('/check_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.result === 'correct') {
            alert('Parabéns! Você acertou o nome do item.');
            fetchRandomCollectible();
        } else {
            alert('Resposta incorreta. Tente novamente!');
            document.getElementById('guess').value = '';
        }
    })
    .catch(error => console.error('Error checking answer:', error));
}
