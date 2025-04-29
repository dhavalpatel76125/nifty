// api/nifty.js

const axios = require('axios');

export default async function handler(req, res) {
  try {
    const response = await axios.get('https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY', {
      headers: {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json'
      }
    });
    res.status(200).json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch Nifty data' });
  }
}
