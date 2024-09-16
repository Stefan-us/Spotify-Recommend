const demoTracks = [
    { name: "Song 1", artist: "Artist 1" },
    { name: "Song 2", artist: "Artist 2" },
    { name: "Song 3", artist: "Artist 3" },
    { name: "Song 4", artist: "Artist 4" },
    { name: "Song 5", artist: "Artist 5" }
];

const demoRecommendations = [
    { name: "Recommended 1", artist: "Artist A" },
    { name: "Recommended 2", artist: "Artist B" },
    { name: "Recommended 3", artist: "Artist C" },
    { name: "Recommended 4", artist: "Artist D" },
    { name: "Recommended 5", artist: "Artist E" }
];

function populateList(elementId, tracks) {
    const list = document.getElementById(elementId);
    tracks.forEach(track => {
        const li = document.createElement('li');
        li.textContent = `${track.name} by ${track.artist}`;
        list.appendChild(li);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    populateList('top-tracks', demoTracks);
    populateList('recommended-tracks', demoRecommendations);
});