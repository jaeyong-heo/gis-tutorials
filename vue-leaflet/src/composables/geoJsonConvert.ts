type RawData = {
    sgg_cd: string;
    emd_cd: string;
    node_wkt: string;
    node_type_cd: string;
    bgng_lnkg_id: number | null;
    lnkg_wkt: string;
    lnkg_id: number;
    node_type: string;
    sgg_nm: string;
    node_id: number;
    emd_nm: string;
    lnkg_len: number | null;
    end_lnkg_id: number | null;
    lnkg_type_cd: string;
  };
  
  type InputData = {
    DESCRIPTION: Record<string, string>;
    DATA: RawData[];
  };
  
  export function convertToGeoJSON(input: InputData): any {
    const features = input.DATA.map((item) => {
      // WKT 형식 "POINT(lng lat)" 파싱
      const match = item.node_wkt.match(/POINT\(([-\d.]+) ([-\d.]+)\)/);
      let coordinates: [number, number] = [0, 0];
  
      if (match) {
        coordinates = [parseFloat(match[1]), parseFloat(match[2])];
      }
  
      return {
        type: "Feature",
        geometry: {
          type: "Point",
          coordinates: coordinates,
        },
        properties: {
          ...item,
        },
      };
    });
  
    return {
      type: "FeatureCollection",
      features: features,
    };
  }
  