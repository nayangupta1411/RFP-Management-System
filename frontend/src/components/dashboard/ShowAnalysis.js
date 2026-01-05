import { useLocation } from 'react-router-dom';

const ShowAnalysis = () => {
  const location = useLocation();
  const { analysis, rating, reason, vendor } = location.state ?? {};

  return (
    <div class="mt-2">
      <p class="formHeading"> Analysis</p>
      <div class="container showVendorRating mt-2">
        <table class="table">
          <tbody>
            <th>Vendor</th>
            <td>{vendor}</td>
            {Object.entries(analysis).map(([key, value]) => (
              <tr>
                <th>{key}</th>
                <td>{value}</td>
              </tr>
            ))}
            <tr>
              <th>rating</th>
              <td>{rating}</td>
            </tr>
            <tr>
              <th>reason</th>
              <td>{reason}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ShowAnalysis;
