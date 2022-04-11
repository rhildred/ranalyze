const cheerio = require('cheerio');
const fs = require('fs');

const $ = cheerio.load(fs.readFileSync('./quiz_d2l_140839.xml'));

const aQuestions = $("item presentation mattext")

for(let n = 0; n < aQuestions.length; n++){
    const sQuestion = $(aQuestions[n]).html();
    let strippedString = sQuestion.replace(/(&lt;([^&gt;]+)&gt;)/gi, ""); 
    console.log(strippedString);
}
