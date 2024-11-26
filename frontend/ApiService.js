import axios from 'axios';

export async function codeCollaboration(userMessage, currentCode) {
  try {
    const response = await axios.post('http://127.0.0.1:5000/api/code-collaboration', {
      user_message: userMessage,
      current_code: currentCode
    },
    {
      headers: {
        'Content-Type': 'application/json',
      }
    });
    return response.data;
  } catch (error) {
    console.error('Error in codeCollaboration:', error);
    return { error: error.message };
  }
}

export async function quickAction(action, currentCode) {
  try {
    const response = await axios.post('http://127.0.0.1:5000/api/quick-action', {
      action: action,
      current_code: currentCode
    },{
    headers: {
      'Content-Type': 'application/json',
    }
  });
    return response.data;
  } catch (error) {
    console.error('Error in quickAction:', error);
    return { error: error.message };
  }
}
