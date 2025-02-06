import "dotenv/config";
import express from 'express';
import Queue from './app/lib/Queue';
import Mailcontroller from './app/controllers/Mailcontroller';

const app = express();

app.use(express.json());
app.post('/send', Mailcontroller.store);

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});