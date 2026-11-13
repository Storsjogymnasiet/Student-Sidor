const images = [
    "asd",
    "ip.png",
    "mosaic.png",
    "website.png",


    "historia.png",
    "arpa.png",

];

const texts = [
    "Sveriges första hemsida skapades 1993 av datorföreningen Lysator på Linköpings universitet. Den innehöll information om föreningen och låg på www.lysator.liu.se. Webbplatsen finns fortfarande kvar.",
    "En IP-adress är en adress som identifierar en enhet på ett nätverk. DNS översätter webbadresser, som googlecom, till IP-adresser Det behövs eftersom det är mycket enklare för människor att komma ihåg namn än siffror.",
    "NCSA Mosaic kom 1993 och blev en av de första stora webbläsarna. Den gjorde webben enklare att använda och kunde visa bilder tillsammans med text. Det hjälpte webben att bli populär",
    "Den första webbsidan var info.cern.ch och skapades omkring 1990 av Tim Berners-Lee. Den innehöll information om World Wide Web och hur man kunde använda det. År 1991 blev webben tillgänglig för fler människor.",
    "Tim Berners-Lee var en brittisk forskare som arbetade på CERN. Han skapade World Wide Web och började utveckla det 1989. Han ville göra det enklare för forskare att dela information genom webbsidor och länkar.",
    "ARPANET var ett tidigt datornätverk som skapades av den amerikanska organisationen ARPA. Det startade 1969 och användes för att koppla ihop datorer på olika forskningsplatser. ARPANET blev en viktig grund för det Internet vi använder idag, första medelen var från Stanford research. 1983 arpa stänged av"

]

const titles = [
    "SVERIGES FÖRSTA HEMSIDAN",
    "IP ADDRESS? DNS?",
    "FÖRSTA STÖRSTA WEBBSIDAN",
    "FÖRSTA WEBBSIDAN",
    "WWW",
    "webbens historia",
]

const sources = [
 
]


let number = 0;

button.addEventListener("click",
    function () {
        number = number + 1;
        text.textContent = texts[number]
        title.textContent = titles[number]
        image.src = "images/" + images[number]
        sources.textContent = sources[number]
        
})    

