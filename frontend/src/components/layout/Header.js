import { useNavigate } from 'react-router-dom';

export default function Header(props) {
  const navigate = useNavigate();

  const onRequestPage = () => {
    navigate('/dashboard/getRequest');
  };

  const onResponsePage = () => {
    navigate('/dashboard/getResponse');
  };

  return (
    <nav class="navbar navbar-secondary bg-secondary px-3 py-2">
      <h4 className="header">{props.title}</h4>
      <div class>
        <button
          class="btn btn-info btn-sm m-2 my-sm-0 p-2"
          onClick={onRequestPage}
        >
          Make Request
        </button>
        <button
          class="btn btn-success btn-sm m-2 my-sm-0 p-2"
          onClick={onResponsePage}
        >
          Check Response
        </button>
      </div>
    </nav>
  );
}
