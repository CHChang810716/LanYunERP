import _axios from "axios"

const be = (baseURL) => {
  const instance = _axios.create({
    baseURL: baseURL || 'http://132.126.126.66:8788/lanyunerpbe',
    timeout: 1000,
  });
  return instance;
}

export { be };
export default be();