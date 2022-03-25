import _axios from "axios"

const be = (baseURL) => {
  const instance = _axios.create({
    baseURL: baseURL || 'http://132.226.126.66:8788/lanyunerpbe',
    timeout: 1000,
  });
  instance.interceptors.request.use(request => {
    console.log('Starting Request', JSON.stringify(request, null, 2))
    return request
  })

  instance.interceptors.response.use(response => {
    console.log('Response:', JSON.stringify(response, null, 2))
    return response
  })
  return instance;
}

export { be };
export default be();