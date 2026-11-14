# Running the kit in an Oracle VirtualBox VM

This guide sets up an **existing** Ubuntu VM in Oracle VirtualBox to run the
participant kit. The examples use the VM name **`sahaa_lsi-SANDIEGO`** — use
your own VM's exact name if it differs. The name is case-sensitive, so it is
always quoted.

Every step is labeled:

- **HOST** — your own computer (Windows, macOS or Linux), in a terminal or PowerShell.
- **UBUNTU VM** — a terminal *inside* the VM.

Nothing here creates a second VM, deletes or replaces this one, or discards
snapshots. Do each phase, check the expected result, then move on.

> Only the public participant kit belongs in this VM. Never copy in a
> receiver, planting scripts, flags, solutions, ingestion tokens, DCE/DCR
> settings or any other organizer material.

---

## Phase 1 · Look before you change anything — HOST

On Windows, `VBoxManage` is usually in `C:\Program Files\Oracle\VirtualBox\`.

```bash
VBoxManage list vms
VBoxManage showvminfo "sahaa_lsi-SANDIEGO" --machinereadable | grep -E '^(VMState|ostype|cpus|memory|nic1)='
VBoxManage snapshot "sahaa_lsi-SANDIEGO" list
```

PowerShell uses `Select-String` instead of `grep`:

```powershell
VBoxManage showvminfo "sahaa_lsi-SANDIEGO" --machinereadable | Select-String '^(VMState|ostype|cpus|memory|nic1)='
```

**Expected:** the VM is listed, `ostype` mentions Ubuntu, and `nic1="nat"`.
Note the CPU and memory values.

## Phase 2 · Snapshot first — HOST

Take a snapshot before changing anything, so you can always get back to
where you started.

```bash
VBoxManage snapshot "sahaa_lsi-SANDIEGO" take "before-polyglot-poisoning" --description "State before the Polyglot Poisoning kit was added"
VBoxManage snapshot "sahaa_lsi-SANDIEGO" list
```

**Expected:** `before-polyglot-poisoning` appears in the list.

## Phase 3 · Resources, only if needed — HOST

The kit itself is light. The participant baseline is **2 vCPUs, 4 GB RAM, a
25 GB dynamically allocated disk, and NAT with no inbound port forwarding**.
If Phase 1 already meets that, skip this phase. A local model (optional) may
need more memory.

Changing hardware requires the VM to be **powered off**, and is a change to
your VM — decide first, then run:

```bash
VBoxManage modifyvm "sahaa_lsi-SANDIEGO" --cpus 2 --memory 4096
VBoxManage modifyvm "sahaa_lsi-SANDIEGO" --nic1 nat
```

Do not add port-forwarding rules; nothing in the kit listens for inbound
connections.

## Phase 4 · Start the VM — HOST

```bash
VBoxManage startvm "sahaa_lsi-SANDIEGO"
```

Log in to Ubuntu. Everything from here is **inside the VM** until Phase 8.

## Phase 5 · Get the kit into the VM — UBUNTU VM

**If the public repository is up to date,** clone it:

```bash
git clone https://github.com/LinguisticSecurityInstitute/polyglot-poisoning.git
cd polyglot-poisoning
```

**If you were given a newer ZIP than GitHub has,** move the ZIP across
instead of cloning an older copy. With NAT, the VM reaches the host's own
loopback address as `10.0.2.2`, so a temporary local web server is enough —
no shared folders or Guest Additions required.

**HOST**, in the folder that holds `polyglot-poisoning.zip`:

```bash
python3 -m http.server 8000 --bind 127.0.0.1     # Windows: py -m http.server 8000 --bind 127.0.0.1
```

**UBUNTU VM:**

```bash
cd ~
wget http://10.0.2.2:8000/polyglot-poisoning.zip
sha256sum polyglot-poisoning.zip                 # compare with the checksum you were given
unzip -q polyglot-poisoning.zip
cd polyglot-poisoning
```

Then stop the HOST web server with **Ctrl+C**.

## Phase 6 · Bootstrap and validate — UBUNTU VM

From the repository root:

```bash
bash vm/bootstrap-ubuntu.sh
```

It installs Python 3 and git only if they are missing, refuses to continue if
it finds organizer-only files, and then runs the three checks. You can also
run them yourself:

```bash
python3 tests/check_setup.py         # expect: SETUP OK
python3 tests/check_repository.py    # expect: REPOSITORY OK
python3 probe.py samples/            # expect: 79 files scanned, 0 would be blocked (score >= 5)
```

**Checkpoint:** all three lines as expected. If one fails, read its message —
do not rename or delete files to make a check pass.

## Phase 7 · Docker, optional — UBUNTU VM

Only after Phase 6 passes. Docker is not needed for the workshop.

```bash
sudo apt-get install -y docker.io
sudo systemctl enable --now docker
sudo docker build -t polyglot-poisoning .
sudo docker run --rm polyglot-poisoning                     # expect: SETUP OK
sudo docker run --rm polyglot-poisoning probe.py samples/   # expect: 79 files scanned, 0 would be blocked
```

Leave the Docker daemon on its local socket. Do not expose it over TCP.

## Phase 8 · Sentinel from the VM's browser — UBUNTU VM

Open the browser inside the VM and sign in to the **Azure portal** with your
ordinary, authorized **DEATHLab** account (not an administrator account).

**Azure portal → Microsoft Sentinel → `deathcon2026-sentinel` → Logs**, set
the time range to **Last 30 days**, then run:

```kql
PolyglotPoisoning_CL
| take 20
```

```kql
PolyglotPoisoning_CL
| where UserPrincipal !endswith "@lb"
| take 20
```

**Checkpoint:** rows come back with seven columns — `TimeGenerated`,
`UserPrincipal`, `Language`, `Variant`, `RiskScore`, `Patterns`,
`PromptPreview`.

**No rows or a permissions error?** Check, in order: you are signed in with
the right account, you opened `deathcon2026-sentinel`, the time range is wide
enough. Then ask an organizer to confirm your account has **Microsoft
Sentinel Reader** (and, if needed, **Log Analytics Reader**) on the
workspace. Participants never need DCE, DCR, stream or ingestion
permissions, and the DCE is not the table — you never query it.

---

## Checklist

| Item | Result |
|---|---|
| VM boots, Ubuntu logs in | PASS / FAIL |
| Snapshot `before-polyglot-poisoning` exists | PASS / FAIL |
| Kit present (cloned or from ZIP) | PASS / FAIL |
| `check_setup.py` → SETUP OK | PASS / FAIL |
| `check_repository.py` → REPOSITORY OK | PASS / FAIL |
| `probe.py samples/` → 79 scanned, 0 blocked | PASS / FAIL |
| Docker build and both runs (optional) | PASS / FAIL / NOT TESTED |
| Sentinel opens with a DEATHLab account | PASS / FAIL |
| Both KQL checks return seven-column rows | PASS / FAIL |
| No organizer files in the VM | PASS / FAIL |

## Day-of launch

1. **HOST:** `VBoxManage startvm "sahaa_lsi-SANDIEGO"`
2. **UBUNTU VM:** `cd ~/polyglot-poisoning && python3 tests/check_setup.py`
3. **UBUNTU VM:** open the browser → Azure portal → Microsoft Sentinel → `deathcon2026-sentinel` → Logs.

## Going back to the snapshot — HOST

Restoring replaces the VM's current state with the snapshot, so anything done
since is lost. Power the VM off first.

```bash
VBoxManage controlvm "sahaa_lsi-SANDIEGO" acpipowerbutton
VBoxManage snapshot "sahaa_lsi-SANDIEGO" restore "before-polyglot-poisoning"
VBoxManage startvm "sahaa_lsi-SANDIEGO"
```
