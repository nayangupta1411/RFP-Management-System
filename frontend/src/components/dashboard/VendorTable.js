import { useNavigate } from 'react-router-dom';

const VendorTable = ({ responses }) => {
  const navigate = useNavigate();

  const handleClick = (analysis, rating, reason, vendor) => {
    console.log('rating before navigate:', rating);
    // Navigate to /showAnalysis and pass data via state
    navigate('/dashboard/showAnalysis', {
      state: { analysis, rating, reason, vendor },
    });
  };

  if (!responses || responses.length === 0) {
    return <p>....</p>;
  }

  return (
    <div class="container ">
      <table className="table">
        <thead>
          <tr>
            <th>#</th>
            <th>Vendor</th>
            <th>Rating</th>
            <th>Status</th>
            <th>View Analysis</th>
          </tr>
        </thead>
        <tbody>
          {responses.map((response, index) => (
            <tr key={index}>
              <th scope="row">{index}</th>
              <td>{response.vendor_email}</td>
              <td>{response.rating ?? 0}/5 ⭐</td>
              <td>{response.recommendation_status ?? 'No Response'}</td>
              <td>
                <button
                  className={`btn ${response.flag ? 'btn-success' : 'btn-danger'}`}
                  disabled={!response.flag}
                  onClick={() =>
                    handleClick(
                      response.analysis,
                      response.rating,
                      response.recommendation_reason,
                      response.vendor_email
                    )
                  }
                >
                  View Details...
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
export default VendorTable;
