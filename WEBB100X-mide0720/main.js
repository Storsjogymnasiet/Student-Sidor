(()=>{
    const htmlEl=document.documentElement;
    const url=new URL(document.currentScript?.src);
    var hash=url.hash.slice(1)||(typeof process!=='undefined'&&process.versions?.electron?'app://':'https://storsjogymnasiet.github.io/Student-Sidor/WEBB100X-mide0720');
    if(hash==="/"){hash="/Student-Sidor/WEBB100X-mide0720";}

    function injectHead(tag,attrs,check){
        if(check&&document.querySelector(check))return;
        const el=document.createElement(tag);
        for(const[k,v]of Object.entries(attrs))el.setAttribute(k,v);
        document.head.appendChild(el);
    }

    injectHead('link',{rel:'stylesheet',href:`${hash}/files/style.css`},`link[href="${hash}/files/style.css"]`);
    injectHead('link',{rel:'icon',href:`${hash}/files/icon.png`},'link[rel="icon"]');

    function loadScript(src){
        if(document.querySelector(`script[src="${src}"]`))return;
        const s=document.createElement('script');
        s.src=src;
        document.body.appendChild(s);
    }

    if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',run);}
    else{run();}
    function run(){loadScript(`${hash}/files/hover.js`);}
})();

function applyTheme(theme){
    htmlEl.setAttribute('data-theme',theme);
    localStorage.setItem('theme',theme);
}