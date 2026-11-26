const legZone = document.getElementById('cat-leg-zone');
const sentinel = document.getElementById('cat-sentinel');
const body = document.createElement('div');
body.className = 'cat-segment';
body.innerHTML = `                      _
            __       / |
            \\ "-..--'_4|_
 _._____     \\ _  _(C "._'._
((^     '"-._( O_ O "._\` '. \\
 \`"'--._     \\  y_     \\   \\|
        '-._  \\_ _  __.=-.__,\\_
            \`'-(" ,("___       \\,_____
                (_,("___     .-./     '
                |   C'___    (5)
                /    \`\`  '---'-'._\`\`\`
               |     \`\`\`    |\`    '"-._
               |    \`\`\`\`    \\-.\`
               |    \`\`\`\`    |  "._ \`\`
               /    \`\`\`\`    |     '-.__
              |     \`\`\`     |
              |    \`\`\`\`    /`;
legZone.appendChild(body);
function addLegs(amount = 30) {
    const fragment = document.createDocumentFragment();
    for (let i = 0; i < amount; i++) {
        const div = document.createElement('div');
        div.className = 'cat-segment';
        div.textContent = "              |    \`\`\`     |";
        fragment.appendChild(div);
    }
    legZone.appendChild(fragment);
}
addLegs(Math.ceil(window.innerHeight / 16.8) + 20);
const observer = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
        addLegs(40);
    }
}, { rootMargin: '400px' });
observer.observe(sentinel);