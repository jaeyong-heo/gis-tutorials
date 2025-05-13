<template>

    <div class="row">
        <BCard border-variant="light" header="basic info" class="text-left w-100">
          <BCardText>   
            <b>위도 :</b> {{ userMK.latitude }} <br>
            <b>경도 :</b> {{ userMK.longtitude }} <br>
            <b>배율 :</b> {{ userMK.zoom }} <br>
            <b>중앙 :</b> {{ userMK.center[0] }}, {{ userMK.center[1] }} <br>
          </BCardText>
          
        </BCard>

        <BCard border-variant="light" header="control" class="text-left w-100">
          <BCardText>   
            <BFormCheckbox id="checkbox-1" v-model="controlStatus.status1" name="checkbox-1" @change="doEmit">
              행정구역
            </BFormCheckbox>

            <BFormCheckbox id="checkbox-2" v-model="controlStatus.status2" name="checkbox-2">
              test
            </BFormCheckbox>

            
          </BCardText>
        </BCard>
        <BButton @click="doCloseController" variant="primary">닫기</BButton>
    </div>
    
</template>

<script setup lang="ts">
import { storeToRefs } from "pinia";
import { useMapStore } from "@/stores/mapStore"
import {ref, defineEmits} from 'vue'
const emit = defineEmits(['controlManage', 'closeController']);

const {userMK, controlStatus} = storeToRefs(useMapStore());



const doEmit = () => {
  emit('controlManage', controlStatus.value)
}
const doCloseController = () => {
  emit('closeController')
}
</script>

<style scoped>

</style>