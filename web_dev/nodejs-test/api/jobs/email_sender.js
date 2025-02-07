import nodemailer from "nodemailer";
import fs from "fs";
import path from "path";
import { differenceInDays } from "date-fns";
import { fileURLToPath } from "url";

// Get __dirname equivalent for ES modules
const __dirname = fileURLToPath(new URL('.', import.meta.url));
const correctedDirname = decodeURIComponent(__dirname); // Decode URL format

async function sendEmail() {

  const customerData = JSON.parse(fs.readFileSync(path.join(__dirname, 'customer_package.json'), 'utf8'));

  const discountExpiresAt = new Date(customerData.discountExpiresAt);
  const currentDate = new Date();

  const daysUntilExpiration = differenceInDays(currentDate, discountExpiresAt);

  console.log(`Days until expiration: ${daysUntilExpiration}`);
  
  // if (daysUntilExpiration === 3) {
  //   console.log("The discount expires in 3 days. Sending email...");

    // Read the HTML email template
    const htmlFilePath = path.join(correctedDirname, "modelo email cobranca CRM.html");
    let htmlContent = fs.readFileSync(htmlFilePath, "utf8");

    // Replace placeholders in the HTML content with actual values from customerData
    htmlContent = htmlContent
      .replace("{$nome}", customerData.nome ) 
      .replace("{$valor}", customerData.totalPrice) 
      .replace("{$venceEm}", customerData.expiresAt) 
      .replace("{$diasVence}", daysUntilExpiration) 
      .replace("{$plano}", `Plano ${customerData.usersQty} usuários`) 
      .replace("{$link_fatura}", `https://link-para-a-fatura.com/${customerData.id}`);

    const transporter = nodemailer.createTransport({
      service: "gmail",
      auth: {
        user: "@gmail.com", // Seu e-mail
        pass: "SUA_SENHA_DE_APLICATIVO", // Senha de aplicativo gerada
      },
    });

    const mailOptions = {
      from: '"Seu Nome" <seuemail@gmail.com>',
      to: "ekkomati0@gmail.com", 
      subject: "Atenção! Sua fatura está disponível", 
      text: "Este é um lembrete para informar que sua fatura está disponível.",
      html: htmlContent, 
    };

    try {
      // Send the email
      const info = await transporter.sendMail(mailOptions);
      console.log("E-mail enviado: " + info.response);
    } catch (error) {
      console.error("Erro ao enviar e-mail:", error);
    }
  // } else {
  //   console.log(`Discount expires in ${daysUntilExpiration} days. No email sent.`);
  // }
}

sendEmail();
