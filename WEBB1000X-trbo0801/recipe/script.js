

function checkStar(starId) {

    for (let i = 1; i <= 5; i++) {
        const star = document.getElementById(`star${i}`)
        star.style.fill = "none"
    }

    for (let i = 1; i <= starId; i++) {
        const star = document.getElementById(`star${i}`)
        star.style.fill = "#ffc400"
    }
}