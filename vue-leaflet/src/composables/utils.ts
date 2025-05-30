// src/api/http.ts

import axios, { type AxiosRequestConfig } from 'axios';

// axios 인스턴스 생성 (옵션 필요시 추가)
const instance = axios.create({
  baseURL: 'http://localhost:7080', // 필요에 따라 baseURL 설정
  timeout: 5000,
  // headers: {'Authorization': 'Bearer ...'}
});

// GET 요청 함수
export async function get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
  try {
    const response = await instance.get<T>(url, config);
    return response.data;
  } catch (error) {
    // 필요에 따라 에러 처리
    throw error;
  }
}

// POST 요청 함수
export async function post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
  try {
    const response = await instance.post<T>(url, data, config);
    return response.data;
  } catch (error) {
    // 필요에 따라 에러 처리
    throw error;
  }
}
