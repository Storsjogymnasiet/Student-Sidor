function startHundredSquareBackground() {
    // Skapa ett element för bakgrunden om det inte finns
    let bgContainer = document.getElementById('split-bg');
    if (!bgContainer) {
        bgContainer = document.createElement('div');
        bgContainer.id = 'split-bg';
        bgContainer.style.position = 'fixed';
        bgContainer.style.top = '0';
        bgContainer.style.left = '0';
        bgContainer.style.width = '100vw';
        bgContainer.style.height = '100vh';
        bgContainer.style.display = 'grid';
        bgContainer.style.gridTemplateColumns = 'repeat(10, 1fr)';
        bgContainer.style.gridTemplateRows = 'repeat(10, 1fr)';
        bgContainer.style.zIndex = '-1'; // Lägg bakom allt annat innehåll
        document.body.prepend(bgContainer);

        // Skapa de 100 rutorna
        for (let i = 1; i <= 100; i++) {
            const square = document.createElement('div');
            square.id = `bg-square-${i}`;
            square.style.width = '100%';
            square.style.height = '100%';
            bgContainer.appendChild(square);
        }
    }

    const helper = () => '#' + Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0');

    setInterval(() => {
        for (let i = 1; i <= 100; i++) {
            document.getElementById(`bg-square-${i}`).style.backgroundColor = helper();
        }
    }, 1000);
}

// Starta funktionen
startHundredSquareBackground();