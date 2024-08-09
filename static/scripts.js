
// Fonction pour ouvrir le modal du QR code
function openQRCodeModal(url) {
    const qrModal = document.getElementById('qrModal');
    const qrCodeContainer = document.getElementById('qrCode');
    qrCodeContainer.innerHTML = ''; // Vider le conteneur du QR code précédent
    const qrUrl = `${window.location.origin}/download/${url.split('/').pop()}`;
    new QRCode(qrCodeContainer, {
        text: qrUrl,
        width: 256,
        height: 256,
    });
    qrModal.classList.add('active');
}

// Fermer le modal du QR code
document.querySelector('.close-btn').onclick = () => {
    document.getElementById('qrModal').classList.remove('active');
};

function addToFavorites(url) {
    fetch('/add-to-favorites', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ photoUrl: url })
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error('Error adding to favorites:', error);
        });
}

function printImage(url) {
    const printWindow = window.open(url, '_blank');
    printWindow.print();
}

function removeFromFavorites(url) {
    fetch('/remove-from-favorites', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ photoUrl: url })
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            location.reload(); // Reload page after removing from favorites
        })
        .catch(error => {
            console.error('Error removing from favorites:', error);
        });
}

document.getElementById('clearFavoritesForm')?.addEventListener('submit', function(event) {
    event.preventDefault();

    fetch('/clear-favorites', {
        method: 'POST',
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            location.reload(); // Reload page after clearing favorites
        })
        .catch(error => {
            console.error('Error clearing favorites:', error);
        });
});


