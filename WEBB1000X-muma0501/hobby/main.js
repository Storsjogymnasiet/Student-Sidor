
const proverbs =[
" fall seven times stand up eight.",
"an inch of time is an inch of gold, but you cannot buy an ich of time with gold",
"vision without action is daydream", 
"if your hugry eat",
"action without vision is nightmare",

];

const quotetext = document.getElementById("quote-text");
const proverbbtn = document.getElementById("btn-proverb");
const loginbtn = document.getElementById("btn-login");
const usernameinput = document.getElementById("username-input");
const welcomeMessage = document.getElementById("welcomeMessage");

proverbbtn.addEventListener("click", function() {
    let randomindex = Math.floor(Math.random() * proverbs.length);
    quotetext.innerText = proverbs[randomindex];
});

loginbtn.addEventListener("click", function() {
    let name = usernameinput.value.trim();

    if (name !== "") {
        welcomeMessage.innerText = "  whats up, " + name + ".";
        usernameinput.value = "";
    } else {
        welcomeMessage.innerText = "invalid name gng, ouuushii .";
    }
});


loginbtn.addEventListener("clicked",  function (){
    loginbtn.classList.add("clicked");
    setTimeout(function() {
        loginbtn.classList.remove("clicked");

    },100);
});

