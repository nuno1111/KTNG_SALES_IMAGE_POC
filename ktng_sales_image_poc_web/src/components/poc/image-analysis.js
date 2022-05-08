import PerfectScrollbar from "react-perfect-scrollbar";
import {
  Box,
  Button,
  Card,
  CardHeader,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";
import { SeverityPill } from "../severity-pill";

export const ImageAnalysis = ({ analysis, ...props }) => {
  return (
    <Card {...props}>
      <CardHeader title="Image Analysis" />
      <PerfectScrollbar>
        <Box sx={{ minWidth: 400 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>POSM 유형</TableCell>
                <TableCell>감지여부</TableCell>
                <TableCell>상대위치</TableCell>
                <TableCell>상태</TableCell>
                <TableCell>신뢰도</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {analysis.map((result) => (
                <TableRow hover key={result.id}>
                  <TableCell>{result.posm}</TableCell>
                  <TableCell>
                    <SeverityPill
                      color={
                        (result.detected === "SUCCESS" && "success") ||
                        (result.detected === "FAIL" && "error") ||
                        "warning"
                      }
                    >
                      {result.detected}
                    </SeverityPill>
                  </TableCell>
                  <TableCell>{result.position}%</TableCell>
                  <TableCell>
                    <SeverityPill
                      color={
                        (result.status === "GOOD" && "success") ||
                        (result.status === "BAD" && "error") ||
                        "warning"
                      }
                    >
                      {result.status}
                    </SeverityPill>
                  </TableCell>
                  <TableCell>{result.confidence}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Box>
      </PerfectScrollbar>
    </Card>
  );
};
