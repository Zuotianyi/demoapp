import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    gender: '',
    dob: '',
    email: '',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:5000/submit', formData);
      console.log(response.data);
      alert('Form submitted successfully');
    } catch (error) {
      console.error('Error details:', error.response);
      alert(`Error submitting form: ${error.message}`);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input
          name="firstName"
          type="text"
          value={formData.firstName}
          onChange={handleChange}
          placeholder="First Name"
        />
        <input
          name="lastName"
          type="text"
          value={formData.lastName}
          onChange={handleChange}
          placeholder="Last Name"
        />
        <div>
          <label>
            <input
              type="radio"
              name="gender"
              value="Male"
              checked={formData.gender === 'Male'}
              onChange={handleChange}
            /> Male
          </label>
          <label>
            <input
              type="radio"
              name="gender"
              value="Female"
              checked={formData.gender === 'Female'}
              onChange={handleChange}
            /> Female
          </label>
        </div>
        <input
          name="dob"
          type="date"
          value={formData.dob}
          onChange={handleChange}
        />
        <input
          name="email"
          type="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="Email"
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default App;