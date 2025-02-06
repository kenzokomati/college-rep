import nodemailer from "nodemailer";
import fs from "fs";
import path from "path";
import { differenceInDays } from "date-fns";

async function sendEmail() {
  const customerData = JSON.parse(fs.readFileSync(path.join(__dirname, 'customer_package.json'), 'utf8'));

  const discountExpiresAt = new Date(customerData.discountExpiresAt);
  const currentDate = new Date();

  const daysUntilExpiration = differenceInDays(discountExpiresAt, currentDate);
  
  if (daysUntilExpiration === 3) {
    console.log("The discount expires in 3 days. Sending email...");

    // Read the HTML email template
    const htmlFilePath = path.join(__dirname, "modelo email cobranca CRM.html");
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
        user: "seuemail@gmail.com", 
        pass: "SUA_SENHA_DE_APLICATIVO", 
      },
    });

    const mailOptions = {
      from: '"Seu Nome" <seuemail@gmail.com>',
      to: "destinatario@gmail.com", 
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
  } else {
    console.log(`Discount expires in ${daysUntilExpiration} days. No email sent.`);
  }
}

sendEmail();
