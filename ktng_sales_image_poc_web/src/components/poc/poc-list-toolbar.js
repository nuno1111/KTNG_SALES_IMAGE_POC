import { Box, Button, CIcon, Typography } from "@mui/material";
import axios from "axios";

export const POCListToolbar = ({ setImgUrl, setAnalysis, ...props }) => {
  // 이미지파일 선택
  function onChangeFile(e) {
    if (e.target.files) {
      const reqUrl = "/api/upload";

      const uploadFile = e.target.files[0];
      const formData = new FormData();
      formData.append("file", uploadFile);

      // 서비스신청 정보 서버통신
      axios
        .post(reqUrl, formData, {
          headers: {
            "Content-Type": `multipart/form-data, boundary=${formData._boundary}`,
          },
        })
        .then((response) => {
          setImgUrl(response.data.downLoadUrl);
          setAnalysis(response.data.analysis);
        });
    }
  }

  return (
    <Box {...props}>
      <Box
        sx={{
          alignItems: "center",
          display: "flex",
          justifyContent: "space-between",
          flexWrap: "wrap",
          m: -1,
        }}
      >
        <Typography sx={{ m: 1 }} variant="h4">
          이미지 분석
        </Typography>
        <Box sx={{ m: 1 }}>
          <Button color="primary" variant="contained" component="label">
            IMAGE UPLOAD
            <input type="file" hidden onChange={onChangeFile} />
          </Button>
        </Box>
      </Box>
    </Box>
  );
};
