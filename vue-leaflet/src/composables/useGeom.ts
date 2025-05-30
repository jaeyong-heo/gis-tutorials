import { ref } from 'vue';
import axios, {isCancel, AxiosError} from 'axios';
import {get, post} from './utils'

export const useGeom = () => {
    

    // GET 요청
    // const userData = await get('/users/1');
    const getGeom = async () => {
        try {
            const result = await get(`/get`);
            return result;
        } catch (error) {
            if (axios.isAxiosError(error)) {
                // Axios 에러 처리
                console.error('Axios error:', error.message);
            } else {
                // 일반 에러 처리
                console.error('Error:', error);
            }
        }
    }

    // POST 요청
    const addGeom = async (data: any) => {        
        try{
            const result = await post('/add', data);
            return result;
        }catch (error) {
            if (axios.isAxiosError(error)) {
                // Axios 에러 처리
                console.error('Axios error:', error.message);
            } else {
                // 일반 에러 처리
                console.error('Error:', error);
            }
        }
        
    }


    return {
        getGeom,
        addGeom,
    };
};


