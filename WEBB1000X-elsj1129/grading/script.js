const searchInput = document.getElementById('searchInput');
const searchButton = document.getElementById('searchButton');
const siteGrid = document.getElementById('siteGrid');
const noResults = document.getElementById('noResults');

const GROUPS = [
    {
        name: 'I-val',
        accent: '#7dd3fc',
        folders: [
            "WEBB1000X-elbr0612",
            "WEBB1000X-erlu1019",
            "webb1-100x--fial0727",
            // Haji
            "WEBB1000X-fite0522",
            "WEBB1000X-kere0213",
            // Leo
            "WEBB1000X-lino0225",
            "WEBB1000X-luhe0812",
            "WEBB1000X-mowi1217",
            "webb1000x-nosl0107",
            "WEBB1000X-olan0720"
        ]
    },
    {
        name: 'EE26+I-val',
        accent: '#c084fc',
        folders: [
            "WEBB1000X-alna0624",
            "webb1000x-anbe0221",
            "WEBB1000X-chha0118",
            "WEBB1000X-mist0524",
            "WEBB1000X-elno0123",
            "WEBB-1000X-hulu0129",
            "WEBB-1000X-lula0214",
            "WEBB100X-mide0720",
            "webb1000x-Mibe0410",
            "WEBB1000X-mila0325",
            "WEBB1000X-miny0319",
            "WEBB1000X-raso0507",
            "WEBB-1000X-riwi0908",
            "WEBB100X-sion0409",
            "WEBB1000X-tiru1119"
        ]
    },
    {
        name: 'EE25',
        accent: '#4ade80',
        folders: [
            "WEBB1000X-aljo0302",
            "WEBB1000X-arla1020",
            "WEBB1000X-ella1002",
            "WEBB1000X-frek1025",
            "WEBB1000X-jafa1104",
            // Jesper
            "WEBB1000X-lega0618",
            "WEBB1000X-live1225",
            "WEBB1000x.-luan0313",
            "WEBB1000X-maas0627",
            "WEBB1000X-makl0716",
            "WEBB1000X-mavi0807",
            "WEBB1000X-muma0501",
            "webb1000x-nier0828",
            "WEBB1000X-Noel0221",
            "WEBB1000X-rane1209",
            "WEBB1000X-trbo0801",
            "WEBB1000X-wisa1007",
            "WEBB1000X-wiwe0421",
            "WEBB1000X-wihe0314"
        ]
    }
];

function normalizeFolderName(folderName) {
    return String(folderName)
        .replace(/^.*\//, '')
        .replace(/\/$/, '')
        .trim();
}

function getGroupForFolder(folderName) {
    const normalizedFolderName = normalizeFolderName(folderName);

    for (const group of GROUPS) {
        const normalizedFolders = group.folders.map(normalizeFolderName);
        if (normalizedFolders.includes(normalizedFolderName)) {
            return group.name;
        }
    }

    return 'Övrigt';
}

function createCard(folderName, assignment) {
    const safeFolderName = normalizeFolderName(folderName);
    const targetPath = assignment ? `${safeFolderName}/${assignment}` : safeFolderName;
    const fullURL = `https://storsjogymnasiet.github.io/Student-Sidor/${targetPath}`;

    const card = document.createElement('a');
    card.className = 'card';
    card.href = fullURL;
    card.target = '_blank';
    card.rel = 'noopener noreferrer';
    card.innerHTML = `
        <div>
            <div class="card-title">${safeFolderName}</div>
            <div class="card-path">/${targetPath}</div>
        </div>
        <div class="card-arrow">Besök sida &rarr;</div>
    `;

    return card;
}

function renderGroups(groupsToRender) {
    siteGrid.innerHTML = '';

    if (groupsToRender.length === 0) {
        noResults.textContent = 'Inga sidor hittades för den valda gruppen.';
        return;
    }

    noResults.textContent = '';

    groupsToRender.forEach(group => {
        const section = document.createElement('section');
        const heading = document.createElement('h2');
        const list = document.createElement('div');

        section.style.borderColor = `${group.accent}55`;
        section.style.boxShadow = `0 12px 28px rgba(0, 0, 0, 0.25), inset 0 0 0 1px ${group.accent}22`;
        heading.textContent = group.name;
        heading.style.color = group.accent;
        heading.style.borderBottomColor = `${group.accent}55`;
        list.className = 'group-list';

        group.items
            .slice()
            .sort((a, b) => normalizeFolderName(a.name).localeCompare(normalizeFolderName(b.name), 'sv'))
            .forEach(folder => {
                list.appendChild(createCard(folder.name, searchInput.value.trim()));
            });

        section.appendChild(heading);
        section.appendChild(list);
        siteGrid.appendChild(section);
    });
}

async function loadSites() {
    const assignment = searchInput.value.trim();

    try {
        const response = await fetch('https://api.github.com/repos/Storsjogymnasiet/Student-Sidor/contents');

        if (!response.ok) {
            throw new Error('Kunde inte hämta innehåll');
        }

        const items = await response.json();
        const studentFolders = items.filter(item => item.type === 'dir' && !item.name.startsWith('.'));

        const matchingGroups = GROUPS.map(group => ({
            ...group,
            items: studentFolders
                .filter(folder => {
                    const groupName = getGroupForFolder(folder.name);
                    if (!groupName || groupName === 'Övrigt') {
                        return false;
                    }

                    if (!assignment) {
                        return group.name === groupName;
                    }

                    const matchesSearch = folder.name.toLowerCase().includes(assignment.toLowerCase()) ||
                        `${folder.name}/${assignment}`.toLowerCase().includes(assignment.toLowerCase());

                    return group.name === groupName && matchesSearch;
                })
                .sort((a, b) => normalizeFolderName(a.name).localeCompare(normalizeFolderName(b.name), 'sv'))
        })).filter(group => group.items.length > 0);

        renderGroups(matchingGroups);

        if (matchingGroups.length === 0) {
            noResults.textContent = assignment
                ? 'Inga matchande sidor hittades i grupperna.'
                : 'Inga sidor hittades i de definierade grupperna.';
        }
    } catch (error) {
        console.error(error);
        siteGrid.innerHTML = '';
        noResults.textContent = 'Ett fel uppstod när sidorna skulle laddas.';
    }
}

searchButton.addEventListener('click', loadSites);
searchInput.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        loadSites();
    }
});

loadSites();
