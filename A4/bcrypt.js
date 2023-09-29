const bcrypt = require('bcryptjs');
const axios = require('axios');

exports.handler = async (event) => {


  const passed_value = event.input;
  // Below code in line 9 has been referred from https://stackoverflow.com/questions/34476754/what-encodings-does-buffer-tostring-support and https://nodejs.org/docs/latest/api/buffer.html#buffer_buffer.
  const utf_value = Buffer.from(passed_value,'utf-8').toString('utf-8');
  //Below code in line 11 has been referred from https://blog.logrocket.com/password-hashing-node-js-bcrypt/ and https://www.npmjs.com/package/bcrypt.
  const output_string = await bcrypt.hash(utf_value, await bcrypt.genSalt());

    const send_back = {
    banner: "B00946400",
    result: output_string,
    arn: "arn:aws:lambda:us-east-1:541064286200:function:Bcrypt_Hashing",
    action: "bcrypt",
    value: passed_value
  };
  //Below code from line 21 - 30 has been referred from https://stackabuse.com/making-asynchronous-http-requests-in-javascript-with-axios/.
  try {
    const send_back_url = await axios.post("https://v7qaxwoyrb.execute-api.us-east-1.amazonaws.com/default/end", send_back);
    return {
      output: output_string
    };
  } catch (error) {
    console.error(error);
    return {
      error: "Error."
    };
  }
};


