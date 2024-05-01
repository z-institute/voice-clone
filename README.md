# Voice Clone Example

1. Go to https://replicate.com/cjwbw/openvoice?prediction=nv4z2r53f9rgj0cf6f9sssjfq4 and upload your own voice clip
2. Create the `.env` file according to `.env.example`
3. Run the following command

```bash
python app.py
python server.py
```

4. Try to call the api

```bash
curl -X POST http://localhost:8800/generate_audio \
-H "Content-Type: application/json" \
-d '{"text": "哈哈哈～晚安拉"}'

```
