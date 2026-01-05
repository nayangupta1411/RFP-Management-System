import { useState, useEffect } from 'react';
import Select from 'react-select';
import axios from 'axios';
import vendors from '../mail/vendorEmail';

const Request = () => {
  const [requestData, setRequestData] = useState({
    name: '',
    org: '',
    email: '',
    contact: '',
    vendor: [],
    message: '',
  });

  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  const validateEmail = (email) => {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
  };

  const validatePhone = (phone) => {
    const regex = /^[0-9]{10}$/;
    return regex.test(phone);
  };

  useEffect(() => {
    if (successMsg) {
      const timer = setTimeout(() => setSuccessMsg(''), 2000);
      return () => clearTimeout(timer);
    }
  }, [successMsg]);

  useEffect(() => {
    if (errorMsg) {
      const timer = setTimeout(() => setErrorMsg(''), 2000);
      return () => clearTimeout(timer);
    }
  }, [errorMsg]);

  const url = 'http://127.0.0.1:5000/dashboard/request';

  const [validated, setValidated] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setValidated(true);

    if (
      requestData.name &&
      requestData.org &&
      validateEmail(requestData.email) &&
      validatePhone(requestData.contact) &&
      requestData.vendor &&
      requestData.message
    ) {
      const axiosPromise = axios.post(url, requestData, {
        headers: { 'Content-Type': 'application/json; charset=utf-8' },
        responseType: 'json',
      });
      axiosPromise
        ?.then((res) => {
          console.log('Status:', res.status);
          console.log('Response data:', res.data);
          setSuccessMsg('Form submitted successfully!');
          setErrorMsg('');
          setRequestData({
            name: '',
            org: '',
            email: '',
            contact: '',
            vendor: [],
            message: '',
          });
          setValidated(false);
        })
        .catch(function (error) {
          console.error(error);
          setErrorMsg('Failed to submit! Try again.');
          setSuccessMsg('');
        });
    }
  };

  const handleChange = (e) => {
    setRequestData({
      ...requestData,
      [e.target.id]: e.target.value,
    });
  };

  return (
    <div class="page-container">
      <div class="container-fluid my-2 formStyle col-lg-6">
        {/* Success alert */}{' '}
        {successMsg && (
          <div className="alert alert-success alert-popup" role="alert">
            {successMsg}
          </div>
        )}
        {/* Error alert */}
        {errorMsg && (
          <div className="alert alert-danger alert-popup" role="alert">
            {errorMsg}{' '}
          </div>
        )}
        <form noValidate onSubmit={handleSubmit}>
          <div class="container-fluid formHeading my-3">RFP Request</div>
          <div class="formDataStyle">
            <div class="row">
              <div class="container-fluid col-lg-6">
                {/*Name */}
                <div class="mb-2">
                  <label htmlFor="name">Name</label>
                  <input
                    type="text"
                    className={
                      'form-control ' +
                      (validated
                        ? requestData.name
                          ? 'is-valid'
                          : 'is-invalid'
                        : '')
                    }
                    id="name"
                    placeholder="Enter name"
                    value={requestData.name}
                    onChange={handleChange}
                    required
                  />
                  <div className="invalid-feedback">
                    Please enter your name.
                  </div>
                </div>
              </div>
              <div class="container-fluid col-lg-6">
                {/* Organization */}
                <div className="mb-2">
                  <label htmlFor="org">Organization</label>
                  <input
                    type="text"
                    className={
                      'form-control ' +
                      (validated
                        ? requestData.org
                          ? 'is-valid'
                          : 'is-invalid'
                        : '')
                    }
                    id="org"
                    placeholder="Enter organization/company"
                    value={requestData.org}
                    onChange={handleChange}
                    required
                  />
                  <div className="invalid-feedback">
                    Please enter your organization name.
                  </div>
                </div>
              </div>
            </div>

            <div class="row">
              <div class="container-fluid col-lg-6">
                {/* Email */}
                <div className="mb-2">
                  <label htmlFor="email">Email</label>

                  <input
                    type="email"
                    className={
                      'form-control ' +
                      (validated
                        ? validateEmail(requestData.email)
                          ? 'is-valid'
                          : 'is-invalid'
                        : '')
                    }
                    id="email"
                    name="email"
                    placeholder="Enter email"
                    value={requestData.email}
                    onChange={handleChange}
                    required
                  />
                  <div className="invalid-feedback">
                    Please enter your correct email.
                  </div>
                </div>
              </div>
              <div class="container-fluid col-lg-6">
                {/* Contact  */}
                <div className="mb-2">
                  <label htmlFor="contact">Contact No.</label>

                  <input
                    type="tel"
                    className={
                      'form-control ' +
                      (validated
                        ? validatePhone(requestData.contact)
                          ? 'is-valid'
                          : 'is-invalid'
                        : '')
                    }
                    id="contact"
                    pattern="[0-9]{3}-[0-9]{2}-[0-9]{3}"
                    placeholder="Enter contact no."
                    value={requestData.contact}
                    onChange={handleChange}
                    required
                  />
                  <div className="invalid-feedback">
                    Please enter a valid 10-digit phone number
                  </div>
                </div>
              </div>
            </div>

            <div class="mb-2">
              <label htmlFor="vendor">Vendor</label>
              <Select
                inputId="vendor"
                classNamePrefix="react-select"
                value={requestData.vendor}
                className={
                  validated
                    ? requestData.vendor.length > 0
                      ? 'is-valid'
                      : 'is-invalid'
                    : ''
                }
                onChange={(selected) =>
                  setRequestData((prev) => ({ ...prev, vendor: selected }))
                }
                options={vendors}
                isMulti
                required
              />
              <div className="invalid-feedback">
                Please select atleast one vendor
              </div>
            </div>

            {/* Request */}
            <div className="mb-2">
              <label htmlFor="message">Request</label>
              <textarea
                className={
                  'form-control ' +
                  (validated
                    ? requestData.message
                      ? 'is-valid'
                      : 'is-invalid'
                    : '')
                }
                id="message"
                value={requestData.message}
                onChange={handleChange}
                placeholder="Enter your requirement"
                rows="3"
                required
              />
              <div className="invalid-feedback">Please enter a message.</div>
            </div>
          </div>

          <button className="btn btn-primary my-3" type="submit">
            Submit Request
          </button>
        </form>
      </div>
    </div>
  );
};

export default Request;
