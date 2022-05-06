import Image from "next/image";
import {
  Box,
  Card,
  CardContent,
  CardHeader,
  Divider,
  CircularProgress,
  LinearProgress,
} from "@mui/material";

export const ImageDetect = ({ loading, imgUrl, ...props }) => {
  return (
    <Card {...props}>
      <CardHeader title="Image Detection" />
      <Divider />
      <CardContent>
        <Box
          sx={{
            width: 1720 / 1.74,
            height: 1080 / 1.74,
            position: "relative",
          }}
        >
          {loading ? <LinearProgress /> : <Image alt="image detect" src={imgUrl} layout="fill" />}
        </Box>
      </CardContent>
    </Card>
  );
};
