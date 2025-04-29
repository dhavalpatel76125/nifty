const express = require('express');
const axios = require('axios');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(cors());

// ✅ Serve root folder (where index.html is directly)
app.use(express.static(__dirname));

// ✅ API Proxy to bypass CORS
app.get('/api/nifty', async (req, res) => {
    try {
        const response = await axios.get('https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY', {
            headers: {
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/json'
            }
        });
        res.json(response.data);
    } catch (error) {
        console.error(error.message);
        res.status(500).json({ message: 'Failed to fetch Nifty data' });
    }
});

app.listen(PORT, () => {
    console.log(`✅ Server running at http://localhost:${PORT}`);
});
