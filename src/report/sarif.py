from typing import Dict, List


class CodeRegion:
    def __init__(self, data: Dict):
        self.data = data

    @property
    def start_line(self) -> int:
        return self.data.get("startLine")

    @property
    def end_line(self) -> int:
        return self.data.get("endLine")

    @property
    def start_column(self) -> int:
        return self.data.get("startColumn")

    @property
    def end_column(self) -> int:
        return self.data.get("endColumn")


class CodeLocation:
    def __init__(self, data: Dict):
        self.data = data

    @property
    def artifact_location_uri(self) -> str:
        return self.data["physicalLocation"]["artifactLocation"]["uri"]

    @property
    def region(self) -> CodeRegion:
        return CodeRegion(self.data["physicalLocation"]["region"])


class CodeFlowLocation:
    def __init__(self, data: Dict):
        self.data = data

    @property
    def artifact_location_uri(self) -> str:
        return self.data["location"]["physicalLocation"]["artifactLocation"]["uri"]

    @property
    def region(self) -> CodeRegion:
        return CodeRegion(self.data["location"]["physicalLocation"]["region"])


class ThreadFlow:
    def __init__(self, data: Dict):
        self.data = data

    @property
    def locations(self) -> List[CodeFlowLocation]:
        return [CodeFlowLocation(code_location) for code_location in self.data.get("locations", [])]


class CodeFlow:
    def __init__(self, data: Dict):
        self.data = data

    @property
    def thread_flows(self) -> List[ThreadFlow]:
        return [ThreadFlow(thread_flow) for thread_flow in self.data.get("threadFlows", [])]


class SarifResult:
    def __init__(self, data: Dict):
        self.data = data

    @property
    def locations(self) -> List[CodeLocation]:
        return [CodeLocation(code_location) for code_location in self.data.get("locations", [])]

    @property
    def code_flows(self) -> List[CodeFlow]:
        return [CodeFlow(code_flow) for code_flow in self.data.get("codeFlows", [])]


class SarifRun:
    def __init__(self, data: Dict):
        self.data = data

    @property
    def results(self) -> List[SarifResult]:
        return [SarifResult(result) for result in self.data["results"]]


class SarifReport:
    def __init__(self, data: Dict):
        self.data = data

    @property
    def runs(self) -> List[SarifRun]:
        return [SarifRun(run) for run in self.data.get("runs", [])]
