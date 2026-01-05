import { useEffect, useRef, useState } from 'react';
import VendorTable from './VendorTable';

const Response = () => {
  const [requests, setRequests] = useState([]);
  const [isVisible, setIsVisible] = useState(false);
  const [responses, setResponses] = useState([]);
  const [selectedRequest, setSelectedRequest] = useState(null);
  const [hasFetched, setHasFetched] = useState(false);

  const fetchedRef = useRef(false);

  useEffect(() => {
    if (fetchedRef.current) return;
    fetchedRef.current = true;

    fetch('http://127.0.0.1:5000/dashboard/getRequests')
      .then((res) => res.json())
      .then((data) => {
        console.log('api response data: ', data);
        setRequests(data);
      })
      .catch((err) => console.error('Fetch error : ', err));
  }, []);

  const formatToIST = (utcDate) => {
    return new Intl.DateTimeFormat('en-IN', {
      timeZone: 'Asia/Kolkata',
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true,
    }).format(new Date(utcDate));
  };

  const fetchResponses = async (uid, vendors) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/dashboard/response', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ uid: uid, vendors: vendors }), // send uid in request body
      });

      const data = await response.json();
      setResponses(data);
      console.log(data); // do something with fetched data
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  useEffect(() => {
    if (!isVisible || !selectedRequest || hasFetched) return;

    fetchResponses(selectedRequest.uid, selectedRequest.receivers);

    setHasFetched(true);
  }, [hasFetched, isVisible, selectedRequest]);

  return (
    <div class="container mt-3 ">
      {requests.map((content, index) => (
        <div class="card mb-2">
          <div class="card-body">
            <div class="row">
              <div class="col-lg-3 text-left">
                <h6 class="card-title">{content.uid}</h6>
                <h6 class="card-subtitle mb-2 text-muted">
                  {formatToIST(content.created_at.$date)}
                </h6>
              </div>
              <div class="col-lg-6 text-center">
                <p class="card-text font-weight-bold">
                  {content.subject.split(':').slice(1).join(':').trim()}
                </p>
              </div>
              <div class="col-lg-3 text-end">
                <button
                  class="btn btn-primary"
                  onClick={() => {
                    setIsVisible((prev) => !prev);
                    setSelectedRequest({
                      uid: content.uid,
                      receivers: content.receivers,
                    });
                    setHasFetched(false);
                  }}
                >
                  Check Response
                </button>
              </div>
            </div>

            {isVisible && <VendorTable responses={responses} />}
          </div>
        </div>
      ))}
    </div>
  );
};

export default Response;
