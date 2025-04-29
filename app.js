const express = require('express');
const axios = require('axios');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = 3000;

// Allow CORS (optional if serving frontend from same server)
app.use(cors());

// Serve static files (your frontend) from 'public' folder
app.use(express.static(path.join(__dirname)));

// Proxy route to fetch NSE data
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

// Start server
app.listen(PORT, () => {
    console.log(`✅ Server running at http://localhost:${PORT}`);
});
